import data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")

        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, 'button.round')
    comfort_rate_icon = (By.XPATH, "//div[@class='tcard-title' and text ()='Comfort']")
    phone_number_button = (By.CSS_SELECTOR, ".np-button")
    phone_number_field = (By.ID, "phone")
    next_button = (By.CSS_SELECTOR, ".button.full")
    sms_confirmation_button = (By.XPATH, "//button[contains(@class, 'button') and text()='Confirmar']")
    sms_code_field = (By.ID,"code")
    # Elementos para la tarjeta
    payment_method_text = (By.CLASS_NAME, 'pp-text')  # Botón "Metodo de pago"
    add_card_title = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")  # Botón "Agregar tarjeta"
    card_number_input = (By.ID, 'number')  # Campo número de tarjeta
    card_code_input = (By.CSS_SELECTOR, 'input.card-input[name="code"]')   # Campo CVV
    card_add_button = (By.XPATH, "//button[text()='Agregar']")  # Botón "Agregar"
    #card_close_button = (By.CSS_SELECTOR, 'div.section.active button.close-button.section-close') #cerrar ventana de agregar tarjeta
    comment_input = (By.ID, 'comment') #final punto 5
    switch_button = (By.CLASS_NAME, "switch")  # Contenedor del botón
    switch_button_input = (By.CLASS_NAME, "switch-input")  # Checkbox interno
    ice_cream_counter = (By.CLASS_NAME, "counter")  # Contenedor del contador
    ice_cream_plus_button = (By.CLASS_NAME, "counter-plus")  # Botón para aumentar
    ice_cream_value = (By.CLASS_NAME, "counter-value")
    reserve_button = (By.XPATH, "//button[contains(@class, 'smart-button')]")
    confirmation_modal = (By.CSS_SELECTOR, 'div.modal.active')
    #9
    reserve_button_main = (By.CSS_SELECTOR, ".smart-button-main")  # Botón de reservar
    countdown_model = (By.XPATH, "//div[contains(@class, 'order-header-time')]")
    overlay = (By.CSS_SELECTOR, "div.overlay")



    def __init__(self, driver):

        self.driver = driver


    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_taxi_button(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        )
    def click_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_rate_icon(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.comfort_rate_icon)
        )
    def click_comfort_rate_icon(self):
        self.get_comfort_rate_icon().click()


    def get_phone_text_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.phone_number_button)
        )
    def click_phone_text_field(self):
        self.get_phone_text_field().click()

    def  get_phone_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.phone_number_field)
        )
    def set_phone_number(self, phone):
        self.get_phone_number_field().send_keys(phone)

    def get_next_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.next_button)
        )
    def click_on_next_button(self):
        self.get_next_button().click()

    def get_sms_code_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.sms_code_field)
        )
    def set_sms_code(self):
        code = retrieve_phone_code(self.driver)
        self.get_sms_code_field().send_keys(code)

    def click_on_sms_confirmation_button(self):
        self.get_confirmation_button().click()

    def get_confirmation_button(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.sms_confirmation_button)
        )

    def click_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_text)
        ).click()

    def click_add_card(self): # clic en "Agregar tarjeta"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_card_title)
        ).click()

    def get_card_number(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_number_input)
        )
    def set_card_number(self, card_number):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_number_input)
        ).send_keys(card_number)

    def get_card_code(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_code_input)
        )

    def set_card_code(self, card_code):
        code_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.card_code_input)
        )
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)

    def click_add_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.card_add_button)
        ).click()

    def get_comment_value(self):
        return WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(self.comment_input)
    ).get_property('value')

    def set_comment(self, comment):
         WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(self.comment_input)
    ).send_keys(comment)

         # clic en el botón slider
    def click_switch_button(self):
             WebDriverWait(self.driver, 15).until(
                 EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.overlay'))
             )

             switch_button = WebDriverWait(self.driver, 15).until(
                 EC.element_to_be_clickable(self.switch_button)
             )
             self.driver.execute_script("arguments[0].click();", switch_button)

    def is_switch_button_active(self):
             switch_input = WebDriverWait(self.driver, 15).until(
                 EC.presence_of_element_located(self.switch_button_input)
             )
             return switch_input.is_selected()

             # aumentar la cantidad de helados

    def add_ice_creams(self, quantity):
        # Esperar a que el overlay desaparezca
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.overlay'))
        )

        plus_button = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.ice_cream_plus_button)
        )
        for _ in range(quantity):
            self.driver.execute_script("arguments[0].click();", plus_button)

        # obtener la cantidad de helados

    def get_ice_cream_quantity(self):
        value_element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.ice_cream_value)
        )
        return int(value_element.text)

    def click_reserve_button(self):
        try:
            # Esperar a que el overlay desaparezca
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.overlay'))
            )

            # Hacer clic en el botón de reservar usando JavaScript
            reserve_button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.reserve_button)
            )
            self.driver.execute_script("arguments[0].click();", reserve_button)
            return True  # Retorna True si el clic se realizó correctamente
        except Exception as e:
            print(f"Error al hacer clic en el botón de reservar: {e}")
            return False  # Retorna False si hubo un error

    #9

    def wait_for_overlay_to_disappear(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located(self.overlay)
        )

    def click_reserve_button_main(self):
        try:
            # Esperar a que el overlay desaparezca
            self.wait_for_overlay_to_disappear()

            reserve_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(self.reserve_button_main)
            )

            self.driver.execute_script("arguments[0].click();", reserve_button)
        except Exception as e:
            print(f"Error al hacer clic en el botón de reservar: {e}")
            raise

    def wait_for_countdown_to_disappear(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located(self.countdown_model)
        )


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(service=Service(), options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_rate(self):
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate_icon()
        comfort_rate = routes_page.get_comfort_rate_icon().text
        comfort_text = "Comfort"
        assert comfort_rate in comfort_text

    def test_set_phone_number(self):
        self.test_select_comfort_rate()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_text_field()
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number_field().get_property('value') == data.phone_number

        routes_page.click_on_next_button()
        # routes_page.get_next_button().click()
        routes_page.set_sms_code()
        routes_page.click_on_sms_confirmation_button()

        assert routes_page.get_phone_text_field().text == data.phone_number

    def test_add_credit_card(self):
        self.test_set_phone_number()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_add_button()

        assert routes_page.get_card_number().get_property('value') == data.card_number
        assert routes_page.get_card_code().get_property('value') == data.card_code

    def test_set_driver_message(self):
        self.test_add_credit_card()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_comment(data.message_for_driver)

        assert routes_page.get_comment_value() == data.message_for_driver

    def test_switch_button(self):
        self.test_add_credit_card()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_switch_button()

        assert routes_page.is_switch_button_active()

    def test_add_ice_creams(self):
        self.test_switch_button()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_creams(2)

        assert routes_page.get_ice_cream_quantity() == 2

    def test_reserve_taxi(self):
        self.test_add_ice_creams()

        routes_page = UrbanRoutesPage(self.driver)

        assert routes_page.click_reserve_button()

    def test_modal(self):
        self.test_reserve_taxi()

        routes_page: UrbanRoutesPage = UrbanRoutesPage(self.driver)
        routes_page.click_reserve_button_main()
        routes_page.wait_for_countdown_to_disappear()

        assert not routes_page.driver.find_element(*routes_page.countdown_model).is_displayed(), \
            "El modal no cambió de estado correctamente. El contador no se abrió o no se completó correctamente."




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

