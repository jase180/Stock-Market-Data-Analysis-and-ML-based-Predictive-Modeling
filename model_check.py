import joblib
from sklearn.tree import export_graphviz
import graphviz

features = [
    "momentum_rsi",
    "momentum_stoch_rsi",
    "momentum_stoch_rsi_k",
    "momentum_stoch_rsi_d",
    "trend_macd",
    "trend_macd_signal",
    "trend_macd_diff",
    "volume_sma_em",
    "trend_sma_fast",
    "trend_sma_slow"
]

loaded_model = joblib.load('model1.pk1')

print(loaded_model)

dot_data = export_graphviz(loaded_model.estimators_[0], 
                           feature_names=features,
                           class_names=["Down", "Up"],
                           filled=True, rounded=True)
# Visualize the tree
graph = graphviz.Source(dot_data)
graph.render("tree")  # Save to file
graph.view()  # Open in default viewer