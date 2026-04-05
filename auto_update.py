import time
from datetime import datetime
from playwright.sync_api import sync_playwright

# 設定登入資訊，方便日後修改
USER_ID = "F6737"
USER_PASS = "Ayuan.0915"

def run():
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print(f"[{datetime.now()}] 開始執行自動更新任務...")
        
        try:
            # 1. 登入
            page.goto("https://www.cbshow.org.tw/Blog/Login.aspx")
            page.fill("#TB_ID", USER_ID)
            page.fill("#TB_PASS", USER_PASS)
            page.click("#LB_Login")
            page.wait_for_url("https://www.cbshow.org.tw/Blog/Sys/Dept_Maintain.aspx")
            print("登入成功。")
            
            # 獲取當前日期 (格式: YYYY-MM-DD)
            today = datetime.now().strftime("%Y-%m-%d")
            
            def update_page(button_selector, page_name):
                print(f"正在更新: {page_name}...")
                page.click(button_selector)
                page.wait_for_selector("#ctl00_ContentPlaceHolder1_TB_aDate")
                page.fill("#ctl00_ContentPlaceHolder1_TB_aDate", today)
                page.click("#ctl00_ContentPlaceHolder1_LB_EditSave")
                page.wait_for_url("https://www.cbshow.org.tw/Blog/Sys/Dept_Maintain.aspx")
                print(f"{page_name} 更新完成。")

            # 1. 科別簡介 (編輯內文)
            update_page("#ctl00_ContentPlaceHolder1_RL_DeptList__rli0_LB_MainEdit", "科別簡介")
            
            # 2. 組織架構 (編輯內文)
            update_page("#ctl00_ContentPlaceHolder1_RL_DeptList__rli1_LB_MainEdit", "組織架構")
            
            # 3. 團隊介紹 (需先展開顯示內容)
            print("正在展開 團隊介紹 內容...")
            page.click("#ctl00_ContentPlaceHolder1_RL_DeptList__rli2_LB_NF")
            time.sleep(2)
            # 第一個編輯
            update_page("#ctl00_ContentPlaceHolder1_RL_DeptList__rli2_GV_DeptItem_ctl02_LB_Edit", "團隊介紹-項目1")
            # 重新展開顯示內容 (因為更新後會回到列表)
            page.click("#ctl00_ContentPlaceHolder1_RL_DeptList__rli2_LB_NF")
            time.sleep(2)
            # 第二個編輯
            update_page("#ctl00_ContentPlaceHolder1_RL_DeptList__rli2_GV_DeptItem_ctl03_LB_Edit", "團隊介紹-項目2")
            
            # 4. 業務內容 (需先展開顯示內容)
            print("正在展開 業務內容 內容...")
            page.click("#ctl00_ContentPlaceHolder1_RL_DeptList__rli3_LB_NF")
            time.sleep(2)
            update_page("#ctl00_ContentPlaceHolder1_RL_DeptList__rli3_GV_DeptItem_ctl02_LB_Edit", "業務內容")
            
            print(f"[{datetime.now()}] 所有頁面更新任務已成功完成！")
            
        except Exception as e:
            print(f"執行過程中發生錯誤: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
