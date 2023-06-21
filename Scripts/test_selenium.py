from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import traceback


def main(stocks: list, file: str):
    driver = webdriver.Chrome()
    try:
        for stock in stocks:
            driver.get(
                r'https://www.set.or.th/th/market/product/stock/quote/' + stock + r'/financial-statement/company-highlights')
            # time.sleep(1)
            # element = driver.find_element(
            #     By.XPATH, '//*[@id="appbar"]//input[@placeholder="ค้นหาหลักทรัพย์, ข่าว, เนื้อหา"]')

            table = driver.find_element(
                By.XPATH, '//table[./thead/tr/th/div[contains(text(),"งวดงบการเงิน ณ วันที่")]]')

            # extract thead
            thead = table.find_element(by=By.TAG_NAME, value='thead')
            tr = thead.find_element(by=By.TAG_NAME, value='tr')

            list_th = get_row_data(tr=tr, find_tag='th')[1:]

            # extract tbody
            tbody = table.find_element(by=By.TAG_NAME, value='tbody')
            list_tr = tbody.find_elements(by=By.TAG_NAME, value='tr')

            cleaned_data = {}
            for tr in list_tr:
                tr_text = get_row_data(tr=tr, find_tag='td')
                cleaned_data[tr_text[0]] = [to_number(s) for s in tr_text[1:]]

            print()
            print(cleaned_data)
            # find D/E
            DE = get_DE(total_debts=cleaned_data['หนี้สินรวม'],
                        total_equity=cleaned_data['ส่วนของผู้ถือหุ้น'])
            ROA = cleaned_data['ROA (%)']
            ROE = cleaned_data['ROE (%)']
            net_profit = cleaned_data['กำไรสุทธิ']
            profit_rate = cleaned_data['อัตรากำไรสุทธิ (%)']
            profit_per_stock = cleaned_data['กำไรต่อหุ้น (บาท)']

            grade = 0
            if a := average(DE) < 1:
                grade = 3
            elif a < 1.5:
                grade = 2
            elif a < 2:
                grade = 1
            else:
                grade = 0

            output = f"""
      STOCK: {stock}
      header {list_th}
      DE : {average(DE)}
      ROA : {average(ROA)}
      ROE : {average(ROE)}
      net_profit : {average(net_profit)}
      profit_rate : {average(profit_rate)}
      profit_per_stock : {average(profit_per_stock)}
      GRADE = {grade}
      \n\n
          """
            with open(file, 'a', encoding='utf8') as f:
                f.write(output)

    except Exception as e:
        print('e', e)
        traceback.format_exc()
    finally:
        driver.close()


def average(data: list):
    if any(data):
        return sum(data) / len(data)
    return None


def to_number(string: str):
    if (type(string) != str):
        return 0
    elif (s := string.replace(',', '').strip()):
        try:
            return float(s)
        except:
            return 0
    else:
        return 0


def get_row_data(tr: WebElement, find_tag: str):
    tags = tr.find_elements(by=By.TAG_NAME, value=find_tag)
    return [th.text.replace('\n', ' ').strip() for th in tags]


def get_DE(total_debts: list, total_equity: list):
    return [
        debt / e if (e := total_equity[i]) != 0 else None
        for i, debt in enumerate(total_debts)
    ]


if __name__ == "__main__":

    file = r"stock_statement.txt"
    with open(file, 'w', encoding='utf8') as f:
        f.write('=====STOCK STATEMENT=====\n')

    stocks = ['AP', 'AIT', 'ICN', 'LH', 'tisco', 'BEM', 'IFS', 'PM', 'IRPC']
    main(stocks=stocks, file=file)
