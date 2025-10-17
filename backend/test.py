# from langchain.chains import LLMCheckerChain
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# llm = ChatOpenAI(openai_api_key='your_key', temperature=0)
 
# text = """Given the prime factorization of 135135 is \(3^3 \times 5 \times 7 \times 11 \times 13\), the five consecutive odd numbers that multiply to give 135135 can be identified from these factors. The numbers are 11, 13, 15 (which is \(3 \times 5\)), 17, and 19. These numbers are consecutive odd numbers that fit 
# the pattern required and utilize all the prime factors exactly once. Summing these numbers gives \(11 + 13 
# + 15 + 17 + 19 = 75\). Therefore, the sum of the five consecutive odd numbers whose product is 135135 is 75"""

# checker_chain = LLMCheckerChain.from_llm(llm, verbose=True)
 
# print(checker_chain.invoke(text))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn import tree
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置字体为黑体

# 示例数据
data = {
    '员工编号': [1, 2, 3, 4, 5, 6, 7, 8],
    '培训前绩效评分': [70, 60, 80, 90, 75, 65, 85, 95],
    '培训参与度': [80, 70, 90, 85, 75, 60, 95, 80],
    '培训时长': [10, 12, 15, 18, 14, 11, 16, 20],
    '培训后绩效评分': [80, 65, 90, 95, 80, 70, 95, 100],
    '员工满意度': [4, 3, 5, 4, 3, 2, 5, 4],
    '工作经验': [5, 3, 7, 10, 6, 4, 8, 12]
}

df = pd.DataFrame(data)
df['培训效果'] = df['培训后绩效评分'] > df['培训前绩效评分']  # 1 表示提升，0 表示未提升

# 划分特征和目标变量
X = df[['培训前绩效评分', '培训参与度', '培训时长', '员工满意度', '工作经验']]
y = df['培训效果']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建决策树模型
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X_train, y_train)

# 预测和评估
y_pred = clf.predict(X_test)
print("模型准确率:", accuracy_score(y_test, y_pred))
print("分类报告:\n", classification_report(y_test, y_pred))


plt.figure(figsize=(12, 8))
tree.plot_tree(clf, feature_names=X.columns.tolist(), class_names=['未提升', '提升'], filled=True)
plt.show()
