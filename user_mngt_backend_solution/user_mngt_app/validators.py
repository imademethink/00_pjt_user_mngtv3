
import re

EMAIL_REGEX = re.compile(r"^(?=.{5,25}$)[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]{2,}$")
PASSWORD_REGEX = re.compile(r"^[A-Za-z0-9]{6}$")
NAME_REGEX = re.compile(r"^[A-Za-z]{5,25}$")
GENERIC_REGEX = re.compile(r"^.{5,25}$")
COUNTRY_CODE_REGEX = re.compile(r"^[0-9]{3}$")
CONTACT_REGEX = re.compile(r"^[0-9]{10}$")
OTP_REGEX = re.compile(r"^[0-9]{6}$")

def validate_email(v): return bool(v and EMAIL_REGEX.fullmatch(v))
def validate_password(v): return bool(v and PASSWORD_REGEX.fullmatch(v))
def validate_name(v): return bool(v and NAME_REGEX.fullmatch(v))
def validate_generic(v): return bool(v and GENERIC_REGEX.fullmatch(v))
def validate_country_code(v): return bool(v and COUNTRY_CODE_REGEX.fullmatch(v))
def validate_contact(v): return bool(v and CONTACT_REGEX.fullmatch(v))
def validate_otp(v): return bool(v and OTP_REGEX.fullmatch(v))
