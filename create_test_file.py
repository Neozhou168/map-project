"""
Quick script to generate a sample Excel file for testing
"""
import pandas as pd

# Sample data
data = {
    '城市': ['南京', '上海', '北京', '深圳', '杭州'],
    '景点': ['先锋书店', '外滩', '故宫', '深圳湾公园', '西湖']
}

df = pd.DataFrame(data)
df.to_excel('test_venues.xlsx', index=False)
print("✅ Created test_venues.xlsx with sample data")
print("\nSample content:")
print(df)
