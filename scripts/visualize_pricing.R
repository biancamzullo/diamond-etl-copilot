suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

args <- commandArgs(trailingOnly = TRUE)
input_csv <- args[1]
output_png <- args[2]

df <- read.csv(input_csv)

p <- ggplot(df, aes(x = carat, y = wholesale_cost)) +
  geom_vline(xintercept = c(1.0, 1.5, 2.0, 3.0), linetype = "dashed", color = "#D1D5DB", size = 0.6) +
  stat_smooth(method = "loess", color = "#1F2937", fill = "#E5E7EB", alpha = 0.5, formula = y ~ x) +
  geom_point(aes(color = is_anomaly, size = is_anomaly), alpha = 0.8) +
  scale_color_manual(values = c("FALSE" = "#2563EB", "TRUE" = "#EF4444")) +
  scale_size_manual(values = c("FALSE" = 2.5, "TRUE" = 4.5)) +
  scale_y_continuous(labels = scales::dollar) +
  labs(
    title = "Supplier Pricing Curve & Magic Weight Disparity",
    subtitle = "Dashed lines indicate psychological pricing tiers (1.0, 1.5, 2.0 ct)",
    x = "Carat Weight",
    y = "Wholesale Price (USD)",
    color = "Anomaly Flagged",
    size = "Anomaly Flagged"
  ) +
  theme_minimal(base_family = "sans") +
  theme(plot.title = element_text(face = "bold", size = 14), legend.position = "bottom")

ggsave(output_png, plot = p, width = 8, height = 5, dpi = 300)