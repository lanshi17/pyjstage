def main():
    # 测试导入
    from pyjstage.pyjstage import Pyjstage
    
    print("✅ 成功导入 Pyjstage!")
    print(f"Pyjstage 类: {Pyjstage}")
    
    # 创建实例
    jstage = Pyjstage()
    print(f"✅ 成功创建 Pyjstage 实例!")
    print(f"API 域名: {jstage.domain}")
    
    print("\n🎉 pyjstage 在 Python 3.12 上运行成功!")

if __name__ == "__main__":
    main()
