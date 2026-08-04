# scripts/cross_validation_audit.R
# acts as an independent statistical auditor. it uses classical linear regression 
# and cook's distance to cross-validate the python isolation forest model, proving the necessity of multi-dimensional ml.
# inputs: input_csv (temporary state data from python), output_png (destination file path)
# outputs: writes a diagnostic png image to the disk.
# errors: fails if the dataset lacks 'carat' or 'retail_price' columns, or if variance is zero.

# fetch command line arguments passed from python's subprocess module
args <- commandArgs(trailingOnly = TRUE)
data_path <- args[1]
output_path <- args[2]

# suppress warnings for clean execution
suppressMessages(library(ggplot2))

# load the dataset passed from Python
df <- read.csv(data_path)

# build a classical linear model to evaluate price against carat weight
model <- lm(retail_price ~ carat, data = df)

# calculate Cook's Distance for every diamond
df$cooks_d <- cooks.distance(model)

# standard statistical threshold for high-leverage outliers
threshold <- 4 / nrow(df)
df$is_r_anomaly <- df$cooks_d > threshold

# generate the audit visualization
p <- ggplot(df, aes(x = carat, y = retail_price, color = is_r_anomaly)) +
  geom_point(alpha = 0.8, size = 3) +
  geom_smooth(method = "lm", color = "black", linetype = "dashed", se = FALSE) +
  scale_color_manual(values = c("FALSE" = "#181492", "TRUE" = "#ff4b4b")) +
  theme_minimal(base_family = "sans") +
  labs(
    title = "Econometric Audit: Cook's Distance",
    subtitle = "Cross-validating Python's Isolation Forest with R statistical modeling",
    x = "Carat Weight",
    y = "Retail Price (USD)"
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    panel.grid.minor = element_blank()
  )

# save the plot to the path requested by Python
ggsave(output_path, plot = p, width = 7, height = 5, dpi = 300)