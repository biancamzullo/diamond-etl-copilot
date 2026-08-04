# suppress startup messages to prevent polluting python's subprocess stdout/stderr capture
suppressPackageStartupMessages({
  # load ggplot2 for advanced, layered data visualizations
  library(ggplot2)
  # load dplyr for any potential dataframe manipulations
  library(dplyr)
})

# fetch command line arguments passed from python's subprocess.run()
args <- commandArgs(trailingOnly = TRUE)
# map arguments to our input (temp csv) and output (destination png) paths
input_csv <- args[1]
output_png <- args[2]

# load the memory state passed from python into an r dataframe
df <- read.csv(input_csv)

# initialize the ggplot object mapping carat weight to wholesale cost
p <- ggplot(df, aes(x = carat, y = wholesale_cost)) +
  # prices jump exponentially at these thresholds due to consumer demand and rough cutting yields.
  geom_vline(xintercept = c(1.0, 1.5, 2.0, 3.0), linetype = "dashed", color = "#D1D5DB", size = 0.6) +
  # this calculates the expected price curve, making it visually obvious when a diamond deviates from the norm.
  stat_smooth(method = "loess", color = "#1F2937", fill = "#E5E7EB", alpha = 0.5, formula = y ~ x) +
  # plot the actual diamonds. dynamically map color and size to the 'is_anomaly' boolean flag.
  geom_point(aes(color = is_anomaly, size = is_anomaly), alpha = 0.8) +
  # forcefully style the anomalies in stark red to immediately draw the operator's eye
  scale_color_manual(values = c("FALSE" = "#2563EB", "TRUE" = "#EF4444")) +
  scale_size_manual(values = c("FALSE" = 2.5, "TRUE" = 4.5)) +
  # format y axis usd
  scale_y_continuous(labels = scales::dollar) +
  
  # cleanly label the visualization for non-technical operations teams
  labs(
    title = "Supplier Pricing Curve & Magic Weight Disparity",
    subtitle = "Dashed lines indicate psychological pricing tiers (1.0, 1.5, 2.0 ct)",
    x = "Carat Weight",
    y = "Wholesale Price (USD)",
    color = "Anomaly Flagged",
    size = "Anomaly Flagged"
  ) +
  # theme for streamlits ui
  theme_minimal(base_family = "sans") +
  theme(plot.title = element_text(face = "bold", size = 14), legend.position = "bottom")

# export the final rendered plot to the disk so python can retrieve it
# set high dpi (300) for crisp retina-display rendering in the browser
ggsave(output_png, plot = p, width = 8, height = 5, dpi = 300)