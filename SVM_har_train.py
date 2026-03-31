import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# =========================
# 0. 保存路径
# =========================
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

# =========================
# 1. 数据准备
# =========================

# 👉 展平
x_train_svm = x_train.reshape(x_train.shape[0], -1)
x_test_svm = x_test.reshape(x_test.shape[0], -1)

# 👉 标签（one-hot → 类别）
y_train_cls = np.argmax(y_train_hot, axis=1)
y_test_cls = np.argmax(y_test, axis=1)

# =========================
# 2. 标准化
# =========================
scaler = StandardScaler()
x_train_svm = scaler.fit_transform(x_train_svm)
x_test_svm = scaler.transform(x_test_svm)

# =========================
# 3. 构建 SVM 模型
# =========================
model = SVC(
    kernel='rbf',       # 常用
    C=10,               # 正则强度
    gamma='scale',      # 自动
    probability=True
)

# =========================
# 4. 训练
# =========================
model.fit(x_train_svm, y_train_cls)

# =========================
# 5. 训练集评估
# =========================
y_pred_train = model.predict(x_train_svm)

print("\n=== Train Report ===")
print(classification_report(y_train_cls, y_pred_train))

# =========================
# 6. 测试集评估
# =========================
y_pred = model.predict(x_test_svm)

print("\n=== Test Metrics ===")
print("Accuracy:", accuracy_score(y_test_cls, y_pred))
print("Precision:", precision_score(y_test_cls, y_pred, average='weighted'))
print("Recall:", recall_score(y_test_cls, y_pred, average='weighted'))
print("F1-score:", f1_score(y_test_cls, y_pred, average='weighted'))

# =========================
# 7. 混淆矩阵
# =========================
cm = confusion_matrix(y_test_cls, y_pred)
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

labels = ['Clapping', 'Downstairs', 'Jogging','Skipping', 'Running',
          'Sitting', 'Squatting', 'Sweeping', 'Upstairs', 'Waving']

plt.figure(figsize=(10, 8), dpi=300)
ax = sns.heatmap(cm_norm, annot=False, cmap="coolwarm",
                 xticklabels=labels, yticklabels=labels)

for i in range(len(labels)):
    for j in range(len(labels)):
        value = cm_norm[i, j]
        color = 'red' if i == j else 'black'
        ax.text(j+0.5, i+0.5, f"{value:.2f}",
                ha='center', va='center',
                color=color, fontsize=9)

plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Normalized Confusion Matrix (SVM)")

plt.tight_layout()
plt.savefig(os.path.join(save_dir, "svm_confusion_matrix.png"))
plt.close()

# =========================
# 8. 保存模型
# =========================
import joblib
joblib.dump(model, os.path.join(save_dir, "svm_model.pkl"))

print(f"\n✅ SVM训练完成，结果保存在: {save_dir}")