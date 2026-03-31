import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# =========================
# 1. 文件路径（改这里）
# =========================
file_path = r"C:\Users\YourName\Desktop\output.txt"

# 图片保存路径
save_dir = "figures"
os.makedirs(save_dir, exist_ok=True)

# =========================
# 2. 列名
# =========================
columns = [
    "user-id", "date", "time",
    "acc-X", "acc-Y", "acc-Z",
    "ang-X", "ang-Y", "ang-Z",
    "heart-X", "heart-Y",
    "label", "timestamp"
]

# =========================
# 3. 行处理函数
# =========================
def process_line(line):
    items = list(filter(None, line.strip().split()))
    
    if len(items) < len(columns):
        return None
    elif len(items) > len(columns):
        items = items[:len(columns)]
        
    return items

# =========================
# 4. 读取数据
# =========================
data = []
with open(file_path, "r", encoding="utf-8") as file:
    next(file)
    for line in file:
        processed = process_line(line)
        if processed:
            data.append(processed)

df = pd.DataFrame(data, columns=columns)

print("数据读取完成:", df.shape)

# =========================
# 5. 类型转换（不删数据）
# =========================
df['label'] = df['label'].astype(str)

df = df.rename(columns={
    "heart-X": "HR",
    "heart-Y": "SpO2"
})

numeric_cols = [
    "acc-X", "acc-Y", "acc-Z",
    "ang-X", "ang-Y", "ang-Z",
    "HR", "SpO2"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')

# 标签编码
df['label'] = df['label'].fillna("unknown")
label_encoder = LabelEncoder()
df['activityEncode'] = label_encoder.fit_transform(df['label'])

# =========================
# 6. 活动分布
# =========================
plt.figure()
df['label'].value_counts().plot(kind='bar')
plt.title('Activity Distribution')
plt.xticks(rotation=45)
plt.savefig(os.path.join(save_dir, "activity_distribution.png"))
plt.close()

# =========================
# 7. 用户分布
# =========================
plt.figure()
df['user-id'].value_counts().plot(kind='bar')
plt.title('User Distribution')
plt.xticks(rotation=45)
plt.savefig(os.path.join(save_dir, "user_distribution.png"))
plt.close()

# =========================
# 8. 加速度
# =========================
sample = df.dropna(subset=["acc-X", "acc-Y", "acc-Z"]).head(500)

plt.figure()
plt.plot(sample['acc-X'], label='acc-X')
plt.plot(sample['acc-Y'], label='acc-Y')
plt.plot(sample['acc-Z'], label='acc-Z')
plt.title('Acceleration')
plt.legend()
plt.savefig(os.path.join(save_dir, "acceleration.png"))
plt.close()

# =========================
# 9. 角速度
# =========================
sample_ang = df.dropna(subset=["ang-X", "ang-Y", "ang-Z"]).head(500)

plt.figure()
plt.plot(sample_ang['ang-X'], label='ang-X')
plt.plot(sample_ang['ang-Y'], label='ang-Y')
plt.plot(sample_ang['ang-Z'], label='ang-Z')
plt.title('Angular Velocity')
plt.legend()
plt.savefig(os.path.join(save_dir, "angular_velocity.png"))
plt.close()

# =========================
# 10. HR + SpO2
# =========================
sample_hr = df.dropna(subset=["HR", "SpO2"]).head(500)

plt.figure()
plt.plot(sample_hr['HR'], label='HR')
plt.plot(sample_hr['SpO2'], label='SpO2')
plt.title('HR & SpO2')
plt.legend()
plt.savefig(os.path.join(save_dir, "hr_spo2.png"))
plt.close()

# =========================
# 11. HR分布
# =========================
plt.figure()
df.boxplot(column='HR', by='label', rot=45)
plt.title('HR by Activity')
plt.suptitle('')
plt.savefig(os.path.join(save_dir, "hr_distribution.png"))
plt.close()

# =========================
# 12. SpO2分布
# =========================
plt.figure()
df.boxplot(column='SpO2', by='label', rot=45)
plt.title('SpO2 by Activity')
plt.suptitle('')
plt.savefig(os.path.join(save_dir, "spo2_distribution.png"))
plt.close()

# =========================
# 13. HR vs SpO2
# =========================
plt.figure()
plt.scatter(df['HR'], df['SpO2'], alpha=0.2)
plt.title('HR vs SpO2')
plt.xlabel('HR')
plt.ylabel('SpO2')
plt.savefig(os.path.join(save_dir, "hr_vs_spo2.png"))
plt.close()

# =========================
# 14. 编码标签
# =========================
plt.figure()
df['activityEncode'].value_counts().plot(kind='bar')
plt.title('Encoded Labels')
plt.savefig(os.path.join(save_dir, "encoded_labels.png"))
plt.close()

# =========================
# 15. 相关性热力图
# =========================
plt.figure()
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True)
plt.title('Correlation')
plt.savefig(os.path.join(save_dir, "correlation.png"))
plt.close()

print(f"✅ 所有图片已保存到文件夹: {save_dir}")