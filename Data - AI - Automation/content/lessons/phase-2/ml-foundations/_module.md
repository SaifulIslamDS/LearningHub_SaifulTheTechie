**Machine learning (ML)** builds models that learn patterns from past examples to make predictions on new ones. This module is about the **foundations that make ML trustworthy**, not about fancy algorithms: a fair test, no leakage, sensible preprocessing, useful features and the right amount of model complexity. Phase 4 builds on it with many more model types.

The running example is a real business question: **when an order is placed, how likely is it to be cancelled?** The scripts are `17_ml_sklearn_split.py`, `18_ml_leakage_scaling.py` and `19_ml_features_bias_variance.py` (with the shared `ml_data.py`) in [data-science-scripts.zip](../../../downloads/phase-2/data-science-scripts.zip). They use **scikit-learn**.

**By the end of this module you can:** build a scikit-learn pipeline, evaluate it honestly with a held-out test set and the right metric, recognise and prevent data leakage, know when scaling matters, engineer and choose features, and diagnose under- and overfitting.
