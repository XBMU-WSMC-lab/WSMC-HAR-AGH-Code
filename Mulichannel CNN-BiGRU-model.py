import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# =========================
# 1. 模型定义
# =========================
def Multi_heads_DilatedCNN(input_size=(128, 8), num_classes=10):
    inputs = tf.keras.Input(shape=input_size)

    # ===== 多头CNN =====
    x1 = tf.keras.layers.Conv1D(32, 7, padding='same', activation='relu')(inputs)
    x1 = tf.keras.layers.BatchNormalization()(x1)
    x1 = tf.keras.layers.Conv1D(64, 7, padding='same', activation='relu')(x1)
    x1 = tf.keras.layers.BatchNormalization()(x1)

    x2 = tf.keras.layers.Conv1D(64, 5, padding='same', activation='relu')(inputs)
    x2 = tf.keras.layers.BatchNormalization()(x2)
    x2 = tf.keras.layers.Conv1D(128, 5, padding='same', activation='relu')(x2)
    x2 = tf.keras.layers.BatchNormalization()(x2)

    x3 = tf.keras.layers.Conv1D(128, 3, padding='same', activation='relu')(inputs)
    x3 = tf.keras.layers.BatchNormalization()(x3)
    x3 = tf.keras.layers.Conv1D(256, 3, padding='same', activation='relu')(x3)
    x3 = tf.keras.layers.BatchNormalization()(x3)

    concat = tf.keras.layers.Concatenate(axis=-1)([x1, x2, x3])

    # ===== BiGRU =====
    x = tf.keras.layers.Bidirectional(tf.keras.layers.GRU(128, return_sequences=True))(concat)
    x = tf.keras.layers.Bidirectional(tf.keras.layers.GRU(64, return_sequences=True))(x)

    # ===== Attention =====
    attn = tf.keras.layers.Attention()([x, x])
    x = tf.keras.layers.Add()([x, attn])
    x = tf.keras.layers.LayerNormalization()(x)

    # ===== 分类头 =====
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128)(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    x = tf.keras.layers.Dense(64)(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.ReLU()(x)

    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    return tf.keras.Model(inputs, outputs)

# =========================
# 2. 加载数据（你需要提前准备好）
# =========================
# 必须提前定义：
# x_train, y_train_hot, x_test, y_test

# =========================
# 3. 构建模型
# =========================
model = Multi_heads_DilatedCNN(input_size=(128, 8), num_classes=10)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001, amsgrad=True),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# =========================
# 4. 训练
# =========================
history = model.fit(
    x_train, y_train_hot,
    batch_size=64,
    epochs=50,
    verbose=1
)

# =========================
# 5. 训练曲线
# =========================
plt.figure(figsize=(6, 4))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['loss'], '--', label='Train Loss')
plt.title('Training Curve')
plt.xlabel('Epoch')
plt.legend()
plt.savefig("training_curve.png")
plt.close()

# =========================
# 6. 训练集评估
# =========================
y_pred_train = model.predict(x_train)
y_pred_train_cls = np.argmax(y_pred_train, axis=1)
y_train_cls = np.argmax(y_train_hot, axis=1)

print("\n=== Train Report ===")
print(classification_report(y_train_cls, y_pred_train_cls))

# =========================
# 7. 测试集评估
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
# 8. 混淆矩阵
# =========================
cm = confusion_matrix(y_true, y_pred_cls)
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

labels = ['Claping', 'Downstairs', 'Jogging','Jumping', 'Running',
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
plt.title("Normalized Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

# =========================
# 9. 保存模型
# =========================
model.save("har_model.h5")

print("✅ 训练完成，模型与图片已保存")