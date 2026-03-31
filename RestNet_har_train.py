import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.layers import Input, Conv1D, BatchNormalization, ReLU, Add, GlobalAveragePooling1D, Dense
from tensorflow.keras.models import Model

# =========================
# 0. 保存路径
# =========================
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

# =========================
# 1. ResNet 模型
# =========================
def residual_block(x, filters, kernel_size=3, stride=1):
    shortcut = x

    x = Conv1D(filters, kernel_size, strides=stride, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv1D(filters, kernel_size, padding='same')(x)
    x = BatchNormalization()(x)

    if shortcut.shape[-1] != filters or stride != 1:
        shortcut = Conv1D(filters, 1, strides=stride, padding='same')(shortcut)
        shortcut = BatchNormalization()(shortcut)

    x = Add()([x, shortcut])
    x = ReLU()(x)
    return x


def build_resnet(input_shape=(128, 8), num_classes=10):
    inputs = Input(shape=input_shape)

    x = Conv1D(64, 7, strides=2, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = residual_block(x, 64)
    x = residual_block(x, 64)

    x = residual_block(x, 128, stride=2)
    x = residual_block(x, 128)

    x = residual_block(x, 256, stride=2)

    x = GlobalAveragePooling1D()(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    return Model(inputs, outputs)

# =========================
# 2. 构建模型
# =========================
model = build_resnet(input_shape=(128, 8), num_classes=10)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# =========================
# 3. 训练
# =========================
history = model.fit(
    x_train, y_train_hot,
    batch_size=64,
    epochs=100,
    verbose=1,
)

# =========================
# 4. 训练曲线（完全一致🔥）
# =========================
plt.figure(figsize=(6, 4), dpi=300)

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.plot(history.history['loss'], '--', label='Train Loss')
plt.plot(history.history['val_loss'], '--', label='Val Loss')

plt.xlabel('Epoch')
plt.ylabel('Value')
plt.title('Training Curve')
plt.legend()
plt.grid()

plt.savefig(os.path.join(save_dir, "training_curve.png"))
plt.close()

# =========================
# 5. 训练集评估
# =========================
y_pred_train = model.predict(x_train)
y_pred_train_cls = np.argmax(y_pred_train, axis=1)
y_train_cls = np.argmax(y_train_hot, axis=1)

print("\n=== Train Report ===")
print(classification_report(y_train_cls, y_pred_train_cls))

# =========================
# 6. 测试集评估（完全一致）
# =========================
y_pred = model.predict(x_test)
y_pred_cls = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

print("\n=== Test Metrics ===")
print("Accuracy:", accuracy_score(y_true, y_pred_cls))
print("Precision:", precision_score(y_true, y_pred_cls, average='weighted'))
print("Recall:", recall_score(y_true, y_pred_cls, average='weighted'))
print("F1-score:", f1_score(y_true, y_pred_cls, average='weighted'))

# =========================
# 7. 混淆矩阵
# =========================
cm = confusion_matrix(y_true, y_pred_cls)
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
plt.title("Normalized Confusion Matrix")

plt.tight_layout()
plt.savefig(os.path.join(save_dir, "confusion_matrix.png"))
plt.close()

# =========================
# 8. 保存模型（保持一致）
# =========================
model.save(os.path.join(save_dir, "resnet_model.h5"))

print(f"\n✅ ResNet版本训练完成，结果已保存到: {save_dir}")