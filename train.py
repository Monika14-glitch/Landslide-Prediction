import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ==============================
# LOAD DATASET
# ==============================

data = pd.read_csv("landslide_dataset_5000.csv")

print(data.head())

# ==============================
# FEATURES AND LABEL
# ==============================

X = data[['temperature','humidity','moisture','vibration','gyro']]
y = data['class']

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# ==============================
# TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# TRAIN KNN MODEL
# ==============================

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# ==============================
# PREDICTION
# ==============================

y_pred = knn.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report\n", classification_report(y_test, y_pred))

# ==============================
# SAVE MODEL
# ==============================

joblib.dump(knn, "knn_landslide_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("\nModel saved successfully")

# ==============================
# CONFUSION MATRIX
# ==============================

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ==============================
# FEATURE DISTRIBUTION GRAPHS
# ==============================

features = ['temperature','humidity','moisture','vibration','gyro']

for feature in features:
    plt.figure(figsize=(6,4))
    sns.boxplot(x=data['class'], y=data[feature])
    plt.title(feature + " Distribution")
    plt.show()

# ==============================
# PAIRPLOT
# ==============================

sns.pairplot(data, hue="class")
plt.show()