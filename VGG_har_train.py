import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# =========================
# 0. 保存路径
# =========================
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)

# =========================
# 1. VGG-1D 模型
# =========================
def VGG_1D(input_shape=(128, 8), num_classes=10):
    inputs = tf.keras.layers.Input(shape=input_shape)

    # Block 1
    x = tf.keras.layers.Conv1D(64, 3, padding='same', activation='relu')(inputs)
    x = tf.keras.layers.Conv1D(64, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.MaxPooling1D(2)(x)

    # Block 2
    x = tf.keras.layers.Conv1D(128, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.Conv1D(128, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.MaxPooling1D(2)(x)

    # Block 3
    x = tf.keras.layers.Conv1D(256, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.Conv1D(256, 3, padding='same', activation='relu')(x)
    x = tf.keras.layers.MaxPooling1D(2)(x)

    # FC
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.5)(x)

    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    return tf.keras.Model(inputs, outputs)

# =========================
# 2. 构建模型
# =========================
model = VGG_1D(input_shape=(128, 8), num_classes=10)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# =========================
# 3. 训练
# =========================
# x_train: (N, 128, 8)
# y_train_hot: one-hot (N, 10)
# x_test, y_test 同理

history = model.fit(
    x_train, y_train_hot,
    batch_size=64,
    epochs=100,
    verbose=1,
    validation_split=0.2
)

# =========================
# 4. 训练曲线（
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
# 6. 测试集评估
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
# 8. 保存模型
# =========================
model.save(os.path.join(save_dir, "vgg_har_model.h5"))

print(f"\n✅ 所有结果已保存到: {save_dir}")