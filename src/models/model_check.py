import joblib
from sklearn.tree import export_graphviz
import graphviz
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from config.settings import MODEL_PATH, FEATURE_COLUMNS

loaded_model = joblib.load(MODEL_PATH)

print(loaded_model)

dot_data = export_graphviz(loaded_model.estimators_[0],
                           feature_names=FEATURE_COLUMNS,
                           class_names=["Down", "Up"],
                           filled=True, rounded=True)
# Visualize the tree
graph = graphviz.Source(dot_data)
graph.render("tree")  # Save to file
graph.view()  # Open in default viewer