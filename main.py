from app.config import *
from app.metrics import (
    start_metrics_server,
    start_heartbeat,
    ACTIVATIONS_TOTAL,
    ACTIVATIONS_DURATION,
    ACTIVATIONS_QUEUE_SIZE,
    ACTIVATION_CHECKS_TOTAL
)

start_metrics_server(port=9090)
start_heartbeat(interval=30)

import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import time
for_reports='5266773307'

cool_boys=[
    '5266773307',
    '832182441',
    '1492874191',
    '629409289',
    '810513715',
    '987177223',
    '7818075644',
    '5087186034',
    "1274881709",
    "1191561644",
    "6404184054",
    "1133814867",
    "193207332",
    "887302508"
]
current_time = time.time()
bad_boys={
"1234567890":current_time+3600*24
}

ids=[
    '832182441',
    '5266773307',
    '588293874',
     ]

users={
        '5266773307':{'name':'👤 Леонид','route':''},
        '832182441':{'name':'👤 Илья (@bingupluss)','route':''},
    }

auth={
    '832182441':'👤 Илья (@bingupluss)',
    '588293874':'👤 Даниил (@lahtion0v)',
    }

#
people_can_change_role=[
    5266773307,
    832182441,
    987177223,
    741641254
]

people_admin=[
    5266773307,
    987177223,
    832182441,
    6404184054,
    741641254,
    5688316809
]

people_hueplekalo=[
    887302508,
    5087186034,
]


import csv
import telebot
from telebot import types
import time
import shelve
import httplib2 
import apiclient.discovery
import re
from oauth2client.service_account import ServiceAccountCredentials

import os.path
import base64
import email
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from datetime import datetime,timedelta,date, time as datetime_time
import pytz
import pyotp
import os
import json
import sys


import random


import subprocess
import os


import traceback


import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os


import requests
import json
from typing import Dict, Any, Optional
from requests.exceptions import RequestException


import json
import uuid
import shelve
from typing import Dict, List, Any
import os


import base64
import requests
import traceback
from typing import Dict, List, Optional, Any
from telebot import util



def escape_md_v2(text):
    """Экранирует все спецсимволы для безопасной отправки в Telegram MarkdownV2"""
    if not text:
        return ""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', str(text))

class NintendoAccountManager:
    
    def __init__(self, base_url: str, login: str, password: str, for_reports: str, bot):
        self.base_url = base_url.rstrip('/')
        self.for_reports = for_reports
        self.bot = bot
        auth_string = f"{login}:{password}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/json',
            "X-CodeApi-App-Key": "ams-bot1",
            "X-CodeApi-App-Secret": AMS_APP_SECRET
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)

            if response.status_code in [200, 201, 204]:
                if response.text:
                    return response.json()
                return {"ok": True, "status": response.status_code}
            error_data = {
                "ok": False,
                "status_code": response.status_code,
                "error": "API Error"
            }
            
            try:
                error_json = response.json()
                error_data.update(error_json)
            except:
                error_data["error"] = response.text or "Unknown error"
            error_msg = f"AMS API Error [{response.status_code}]: {endpoint}\n{error_data}"
            self.bot.my_bot.send_message(self.for_reports, error_msg)
            
            return error_data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"AMS Request Failed: {endpoint}\n{str(e)}\n{traceback.format_exc()}"
            self.bot.my_bot.send_message(self.for_reports, error_msg)
            
            return {
                "ok": False,
                "error": "RequestException",
                "message": str(e)
            }
        except Exception as e:
            error_msg = f"AMS Unexpected Error: {endpoint}\n{str(e)}\n{traceback.format_exc()}"
            self.bot.my_bot.send_message(self.for_reports, error_msg)
            
            return {
                "ok": False,
                "error": "UnexpectedError",
                "message": str(e)
            }
    
    def get_accounts_list(self, include_disabled: bool = False, limit: int = 10000, offset: int = 0) -> Dict[str, Any]:
        params = {
            "includeDisabled": str(include_disabled).lower(),
            "limit": limit,
            "offset": offset
        }
        
        result = self._request("GET", "/api/ams/ninaccounts/list", params=params)
        
        
        return result
    
    def get_account_id_by_email(self, email: str, include_disabled: bool = False) -> Dict[str, Any]:
        params = {
            "email": email,
            "includeDisabled": str(include_disabled).lower()
        }
        
        return self._request("GET", "/api/ams/ninaccounts/getId", params=params)
    
    def create_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/api/ams/ninaccounts", json=account_data)
    
    def update_account(self, account_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}"
        return self._request("PATCH", endpoint, json=update_data)

    def get_account_usages(self, account_id: str, include_released: bool = False,
                        limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages"
        params = {
            "includeReleased": str(include_released).lower(),
            "limit": limit,
            "offset": offset,
        }
        return self._request("GET", endpoint, params=params)


    def release_usage(self, account_id: str, usage_id: str, reason: str = "") -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages/{usage_id}"
        data = {
            "operation": "release",
            "reason": reason,
        }
        return self._request("PATCH", endpoint, json=data)


    def release_all_usages(self, account_id: str, reason: str = "") -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages"
        data = {
            "operation": "releaseAll",
            "reason": reason,
        }
        return self._request("PATCH", endpoint, json=data)


    
    def record_usage(self, account_id: str, usage_data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages"
        return self._request("POST", endpoint, json=usage_data)
    
    def get_usage_history(self, account_id: str, include_released: bool = True, 
                         limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages"
        params = {
            "includeReleased": str(include_released).lower(),
            "limit": limit,
            "offset": offset
        }
        
        return self._request("GET", endpoint, params=params)
    
    def release_all_usages(self, account_id: str, reason: str = "") -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages"
        data = {
            "operation": "releaseAll",
            "reason": reason
        }
        
        return self._request("PATCH", endpoint, json=data)
    
    def release_usage(self, account_id: str, usage_id: str, reason: str = "") -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/usages/{usage_id}"
        data = {
            "operation": "release",
            "reason": reason
        }
        
        return self._request("PATCH", endpoint, json=data)
    
    
    def find_account_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        result = self.get_account_id_by_email(email)
        
        if result.get("ok"):
            return result
        
        return None

    def get_2fa_code(self, account_id: str) -> Dict[str, Any]:
        endpoint = f"/api/ams/ninaccounts/{account_id}/2fa"
        return self._request("GET", endpoint)





class CyndykShopAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://ps.cyndykshop.su:8443" 
        self.api_key = CyndykShopAPI_key
        login = NintendoAccountManager_login
        password = NintendoAccountManager_password
        auth_string = f"{login}:{password}"
        bot.my_bot.send_message(for_reports, auth_string)
        bot.my_bot.send_message(for_reports, api_key)

        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        self.headers = {
            'Authorization': f'Basic {auth_base64}',
            "Content-Type": "application/json"
        }

        

    def activate_nintendo(self, email: str, code: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/nintendo/Activate"
        payload = {
            "Email": email,
            "Code": code.upper()
        }
        start_time = time.time()
        status_to_record = "unknown"
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                if not response.text:
                    status_to_record = "error"
                    return self._error("Сервер вернул пустой ответ при создании заявки")
                try:
                    data = response.json()
                    task_id = data.get("uuid") or data.get("taskId")
                    if task_id:
                        status_to_record = "success"
                        return {
                            "status": "success",
                            "task_id": task_id,
                            "message": "Заявка принята в обработку",
                            "error_code": None,
                            "data": data,
                        }
                    else:
                        status_to_record = "error"
                        return self._error("UUID заявки не получен от сервера", error_code="NoUUID", data=data)
                except json.JSONDecodeError:
                    status_to_record = "error"
                    return self._error("Неверный формат ответа сервера", error_code="BadJSON", data=response.text[:500])
                    
            if response.status_code == 204:
                status_to_record = "error"
                error_code = response.headers.get("X-Activation-Error-Code", "")
                error_desc = response.headers.get("X-Activation-Error-Description", "")
                try:
                    error_desc = error_desc.encode('latin-1').decode('utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
                if error_code == "NintendoPasskeyNotFound":
                    return self._error("У аккаунта нет активного passkey — активация невозможна.", error_code=error_code, data={"description": error_desc})
                return self._error(error_desc or f"Аккаунт не прошёл проверку ({error_code})", error_code=error_code or "NoContent204")
                
            if response.status_code == 400:
                status_to_record = "error"
                return self._parse_400_activate(response)
                
            if response.status_code == 401:
                status_to_record = "error"
                return self._error("Ошибка авторизации в API. Проверьте ключ доступа.", error_code="Unauthorized401")
                
            if response.status_code == 405:
                status_to_record = "error"
                return self._error("Внутренняя ошибка: использован неверный HTTP-метод", error_code="MethodNotAllowed405")
                
            if response.status_code == 409:
                try:
                    data = response.json()
                except Exception:
                    data = {"raw": response.text[:300]}
                if data.get("error") == "NintendoAccountBusy":
                    status_to_record = "busy"
                    return {
                        "status": "busy",
                        "task_id": None,
                        "message": "Аккаунт сейчас занят другой операцией. Подождите 10–30 секунд и попробуйте снова.",
                        "error_code": "NintendoAccountBusy",
                        "data": data,
                    }
                status_to_record = "error"
                return self._error("Конфликт запроса (409)", error_code="Conflict409", data=data)
                
            if response.status_code == 500:
                status_to_record = "error"
                try:
                    data = response.json()
                    if data.get("error") == "InternalError":
                        return self._error("Ошибка на стороне провайдера. Повторите попытку через пару минут.", error_code="InternalError500")
                    return self._error(f"Внутренняя ошибка сервера: {data}", error_code="ServerError500", data=data)
                except Exception:
                    return self._error("Внутренняя ошибка сервера (500)", error_code="ServerError500", data=response.text[:300])
                    
            status_to_record = "error"
            return self._error(f"Неожиданный ответ от сервера (HTTP {response.status_code})", error_code=f"HTTP_{response.status_code}", data=response.text[:300])
            
        except requests.exceptions.Timeout:
            status_to_record = "timeout"
            return self._error("Сервер не ответил вовремя. Результат неизвестен.", error_code="Timeout")
        except requests.exceptions.ConnectionError:
            status_to_record = "connection_error"
            return self._error("Не удалось подключиться к серверу активации. Проверьте сеть.", error_code="ConnectionError")
        except Exception as e:
            status_to_record = "unknown"
            return self._error(f"Непредвиденная ошибка: {str(e)}", error_code="Unknown")
        finally:
            ACTIVATIONS_DURATION.observe(time.time() - start_time)
            ACTIVATIONS_TOTAL.labels(status=status_to_record).inc()

    def _parse_400_activate(self, response) -> Dict[str, Any]:
        text = (response.text or "").strip()
        content_type = response.headers.get("Content-Type", "")
        if "text/plain" in content_type or not text.startswith("{"):
            error_map = {
                "InputNintendoActivation is required": "Неверный формат запроса к API",
                "Email is required": "Не указан e-mail аккаунта",
                "Code must be 8 symbols": "Код консоли должен содержать 8 символов",
            }
            for pattern, message in error_map.items():
                if pattern in text:
                    return self._error(message, error_code=f"BadRequest400:{pattern}")
            return self._error(f"Ошибка запроса: {text[:200]}", error_code="BadRequest400")
        
        try:
            data = response.json()
            error_key = data.get("error")
            
            json_errors = {
                "NintendoAccountNotFound": "Аккаунт с таким e-mail не найден в базе провайдера",
                "NintendoAccountDisabled": "Аккаунт отключён или требует восстановления пароля",
            }
            if error_key in json_errors:
                return self._error(json_errors[error_key], error_code=error_key, data=data)
            
            return self._error(
                f"Ошибка API: {data.get('detail', error_key or data)}",
                error_code="BadRequest400",
                data=data,
            )
        except Exception:
            return self._error(f"Ошибка запроса: {text[:200]}", error_code="BadRequest400")


    def _error(self, message: str, error_code: str = None, data: Any = None) -> Dict[str, Any]:
        return {
            "status": "error",
            "task_id": None,
            "message": message,
            "error_code": error_code,
            "data": data,
        }

    def get_nintendo_status(self, task_id: str) -> Dict[str, Any]:
        if not task_id:
            return self._status_error("Не передан UUID заявки", error_code="NoUUID")
        
        url = f"{self.base_url}/api/nintendo/GetStatus"
        payload = {"UUID": task_id}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            
            # === 200: Успешный ответ со статусом ===
            if response.status_code == 200:
                if not response.text:
                    return self._status_error(
                        "Сервер вернул пустой ответ",
                        error_code="EmptyResponse",
                    )
                
                try:
                    data = response.json()
                except json.JSONDecodeError:
                    return self._status_error(
                        "Неверный формат ответа статуса",
                        error_code="BadJSON",
                        data=response.text[:300],
                    )
                
                task_status = data.get("TaskStatus")
                
                # Очередь / В обработке
                if task_status in (1, 2):
                    status_text = "в очереди" if task_status == 1 else "в обработке"
                    return {
                        "status": "pending",
                        "task_status": task_status,
                        "final_code": None,
                        "message": f"Заявка {status_text}, ожидаем результата",
                        "error_code": None,
                        "data": data,
                    }
                
                # Успешно завершено
                if task_status == 3:
                    final_code = data.get("FinalCode")
                    return {
                        "status": "success",
                        "task_status": 3,
                        "final_code": final_code,
                        "message": (
                            f"Активация завершена. Код для консоли: {final_code}"
                            if final_code
                            else "Активация завершена (тестовый режим)"
                        ),
                        "error_code": None,
                        "data": data,
                    }
                
                # Неудача / отмена
                if task_status == 4:
                    ext_status = data.get("ExtStatus", "")
                    return self._parse_failed_status(ext_status, data)
                
                # Неизвестный TaskStatus
                return self._status_error(
                    f"Неизвестный статус заявки: {task_status}",
                    error_code=f"UnknownTaskStatus:{task_status}",
                    data=data,
                )
            
            # === 400: Ошибки валидации ===
            if response.status_code == 400:
                text = (response.text or "").strip()
                error_map = {
                    "InputNintendoStatus is required": "Неверный формат запроса статуса",
                    "UUID is required": "Не указан UUID заявки",
                    "UUID must be valid": "Неверный формат UUID заявки",
                }
                for pattern, message in error_map.items():
                    if pattern in text:
                        return self._status_error(message, error_code=f"BadRequest400:{pattern}")
                return self._status_error(f"Ошибка запроса статуса: {text[:200]}", error_code="BadRequest400")
            
            # === 401 ===
            if response.status_code == 401:
                return self._status_error(
                    "Ошибка авторизации в API",
                    error_code="Unauthorized401",
                )
            
            # === 405 ===
            if response.status_code == 405:
                return self._status_error(
                    "Внутренняя ошибка: неверный HTTP-метод",
                    error_code="MethodNotAllowed405",
                )
            
            # === 500 ===
            if response.status_code == 500:
                return self._status_error(
                    "Ошибка на стороне провайдера. Повторите запрос через 5–10 секунд.",
                    error_code="InternalError500",
                    data=response.text[:300],
                )
            
            return self._status_error(
                f"Неожиданный ответ от сервера (HTTP {response.status_code})",
                error_code=f"HTTP_{response.status_code}",
                data=response.text[:300],
            )
        
        except requests.exceptions.Timeout:
            return self._status_error(
                "Сервер статуса не ответил вовремя. Повторите запрос позже.",
                error_code="Timeout",
                retryable=True,
            )
        except requests.exceptions.ConnectionError:
            return self._status_error(
                "Не удалось подключиться к серверу статуса",
                error_code="ConnectionError",
                retryable=True,
            )
        except Exception as e:
            return self._status_error(
                f"Непредвиденная ошибка: {str(e)}",
                error_code="Unknown",
            )


    def _parse_failed_status(self, ext_status: str, data: Dict) -> Dict[str, Any]:
        """Разбор ExtStatus при TaskStatus=4 (неудача)."""
        ext = (ext_status or "").strip()
        
        if ext == "TaskNotFoundByUuid":
            return self._status_error(
                "Заявка не найдена. Проверьте UUID или передайте ситуацию оператору.",
                error_code="TaskNotFoundByUuid",
                data=data,
            )
        
        if "CodeExpiredOrInvalid" in ext:
            return self._status_error(
                "Код консоли устарел или неверен. Запросите новый 8-символьный код с консоли и повторите активацию.",
                error_code="CodeExpiredOrInvalid",
                data=data,
                retryable=True,
            )
        
        if "SupersededByNewRequest" in ext:
            return self._status_error(
                "Заявка была отменена более поздним запросом по этому же аккаунту.",
                error_code="Superseded",
                data=data,
            )
        
        if "Passkey" in ext:
            return self._status_error(
                "У аккаунта нет активного passkey. Требуется ручная настройка.",
                error_code="PasskeyIssue",
                data=data,
            )
        
        message = ext if ext else "Активация не удалась по неизвестной причине"
        return self._status_error(
            f"Активация не удалась: {message}",
            error_code="ActivationFailed",
            data=data,
        )


    def _status_error(self, message: str, error_code: str = None, data: Any = None, retryable: bool = False) -> Dict[str, Any]:
        return {
            "status": "error",
            "task_status": None,
            "final_code": None,
            "message": message,
            "error_code": error_code,
            "data": data,
            "retryable": retryable,  
        }

    def get_account_by_raw_games(self, raw_games: List[str], is_dlc: bool = False, prefix: str = "") -> Dict[str, Any]:
        formatted_games = prepare_games_for_api(raw_games, is_dlc, prefix)
        if not formatted_games:
            return {"status": "error", "error": "No valid games after cleaning"}
        print(f"Ищем аккаунт для игр: {formatted_games}")
        return self.get_account(formatted_games)

    def get_account(self, games: List[str]) -> Dict[str, Any]:
        url = f"{self.base_url}/account/"
        payload = {"games": games}
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data == "no eligible accounts found":
                    return {"status": "no_accounts", "message": "Аккаунты не найдены","target":str(games)}
                return {"status": "success", "data": data,"target":str(games)}
            else:
                return {"status": "error", "error": f"HTTP {response.status_code}", "response": response.text,"target":str(games)}
        except Exception as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}

def debag(txt):
    return 0


class Bot:
    def __init__(self):

        token = BOT_TOKEN

        self.my_bot=telebot.TeleBot(token)
        self.ids=ids
        self.auth=auth
        self.mega_kost={}

        db=shelve.open(BOT_END_DATA_SHELVE)
        self.users=db.get('users',users)
        self.accs=db.get('accs',{})
        self.alarms4t=db.get('alarms4t',{})
        
        self.tegs=db.get("tegs",{"Red Dead Redemption":"#rdr"})
        self.tegs={"Red Dead Redemption":"#rdr"}
        self.maks_tek=db.get('maks_tek',{})

        db.close()
        
        
        
        db=shelve.open(ADMIN_DATA_SHELVE)
        self.auth=db.get('auth',auth)
        self.ids=db.get('ids',ids)
        self.ids=db.get('ids',ids)
        self.people_admin=db.get('people_admin',people_admin)
        self.people_hueplekalo=db.get('people_hueplekalo',people_hueplekalo)
        self.cool_boys=db.get('cool_boys',cool_boys)
        db.close()
        self.people_can_change_role=people_can_change_role
        
        
   

        self.create_button()
        
        self.errors_acc={}

        self.pagination={}
        self.page={}

        self.ams = NintendoAccountManager(
            base_url="https://ps.cyndykshop.su:8443", 
            login=NintendoAccountManager_login,                  
            password=NintendoAccountManager_password,         
            for_reports=for_reports,
            bot=self
        )

    def ams_sync(self, message=None):
        if message:
            self.my_bot.send_message(message.from_user.id, "🔄 Начинаю синхронизацию с AMS...")
        self.my_bot.send_message(for_reports, "🔄 AMS Sync started...")
        result = self.ams.get_accounts_list(include_disabled=False)
        if not result.get("ok"):
            self.my_bot.send_message(for_reports, f"❌ AMS Sync failed: {result}")
            if message:
                self.my_bot.send_message(message.from_user.id, "Ошибка синхронизации")
            return
        items = result.get("items", [])
        email_index = {}
        for key, acc in self.accs.items():
            mail = (acc.get('Почта') or '').strip().lower()
            if mail:
                email_index.setdefault(mail, key)

        synced_count = 0
        for item in items:
            try:


                email = (item.get("email") or "").strip()
                account_code = (item.get("accountCode") or "").strip()
                login_id = (item.get("loginId") or "").strip()   

                old_by_email = email_index.get(email.lower()) if email else None

                if login_id and login_id in self.accs:
                    login_key = login_id         
                elif old_by_email:
                    login_key = old_by_email     
                elif login_id:
                    login_key = login_id          
                else:
                    login_key = account_code or email
                    if not login_key:
                        continue

                acc = self.accs.get(login_key, {'Входы': {}, 'QR': ''})
                acc['Почта'] = email or acc.get('Почта', '')
                acc['Пароль'] = item.get("password") or acc.get('Пароль', '***')
                acc['Игры'] = '\n'.join(item.get("gameTitles", [])) or acc.get('Игры', '')  
                acc['Резервные коды']=""
                if item.get("reserveCodesCount", 0) > 0:
                    acc['Резервные коды'] = '\n'.join(item.get("reserveCodes", []))
                acc['Дополнительно'] = item.get("additionalInfo") or acc.get('Дополнительно', '')

                acc['logins30d'] = item.get('logins30d', 0)
                acc['loginsTotal'] = item.get('loginsTotal', 0)
                acc['lastLogins'] = item.get('lastLogins', '')
                acc['ams_account_id'] = item.get('accountId', '')
                acc['loginId'] = login_id

                self.accs[login_key] = acc
                if email:
                    email_index.setdefault(email.lower(), login_key)
                synced_count += 1
            except Exception:
                import traceback
                error_msg = f"ams_sync item crash: {item.get('email')}\n{traceback.format_exc()}"
                self.my_bot.send_message(for_reports, error_msg)

        self.little_save_data()
        self.my_bot.send_message(for_reports, f"✅ AMS Sync finished. Synced: {synced_count}")
        if message:
            self.my_bot.send_message(message.from_user.id, f"✅ Синхронизировано аккаунтов: {synced_count}")
    def ams_get_acc_by_login(self, login):
        acc = self.accs.get(login, {})
        email = acc.get('Почта', '')
        if not email:
            return None
        
        result = self.ams.get_account_id_by_email(email)
        if result.get("ok"):
            return result
        return None

    def get_vhody(self, acc):
        a = acc.get('logins30d', 0)
        b = acc.get('loginsTotal', 0)
        
        key = str(self.get_day())
        bb = 0
        cc = 0
        for key2 in acc.get('Входы', {}):
            try:
                if int(key) - int(key2) <= 30:
                    bb += acc['Входы'][key2]
                cc += acc['Входы'][key2]
            except (ValueError, TypeError):
                bb,cc = 0, 0
        
        return max(a,bb),max(b,cc)



    def check_date(self,input_string):
        pattern = r"отлег (\d{2}\.\d{2}\.\d{4})"
        match = re.search(pattern, input_string)
        rz=''

        if match:
            date_str = match.group(1)
            date = datetime.strptime(date_str, "%d.%m.%Y")
            current_date = datetime.now()

            if (current_date - date) < timedelta(days=30):
                rz='‼️'
        return rz
    
    def send_to_aegis(self, data: str, timeout: int = 120) -> Optional[Dict[str, Any]]:
        BASE_URL = "https://auto.ps.cyndykshop.su"
        ENDPOINT = "/aegis/" 
        
        url = f"{BASE_URL.rstrip('/')}{ENDPOINT}"
        
    
        headers = {
            'Content-Type': 'text/plain',
            'Accept': 'application/json',
            'x-api-key': AEGIS_API_KEY,  
        }
        
        try:
            response = requests.post(
                url=url,
                headers=headers,
                data=data,
                timeout=timeout,
                verify=True
            )
            
            self.my_bot.send_message(for_reports, f"📤 Отправка TSV на {url}")
            self.my_bot.send_message(for_reports, f"📦 Данные (первые 200 символов): {data[:200]}")
            self.my_bot.send_message(for_reports, f"📥 Статус ответа: {response.status_code}")
            
            if response.status_code in (200, 201, 202): 
                try:
                    result = response.json()
                    return result
                except json.JSONDecodeError:
                    self.my_bot.send_message(for_reports, f"⚠️ Ответ не в JSON: {response.text[:500]}")
                    return {"text": response.text}
            else:
                self.my_bot.send_message(for_reports, f"❌ Ошибка сервера: {response.status_code}")
                self.my_bot.send_message(for_reports, f"Текст ошибки: {response.text[:500]}")
                response.raise_for_status()
                
        except requests.exceptions.Timeout:
            self.my_bot.send_message(for_reports, f"⏰ Таймаут соединения ({timeout} сек)")
            raise RequestException(f"Request timeout after {timeout} seconds")
        except requests.exceptions.ConnectionError:
            self.my_bot.send_message(for_reports, "🔌 Ошибка подключения к серверу")
            raise RequestException("Connection error")
        except requests.exceptions.RequestException as e:
            self.my_bot.send_message(for_reports, f"🚫 Ошибка запроса: {str(e)}")
            raise
        except Exception as e:
            self.my_bot.send_message(for_reports, f"💥 Неожиданная ошибка: {str(e)}")
            raise

    def max_please(self):
        db=shelve.open(MAX_PLEASE_DATA_SHELVE)
        mtimes=db.get("mtimes",[])
        db.close()

        mail='https://console.developers.google.com/cloud-resource-manager'
        token2= GOOGLE_TOKEN
        CREDENTIALS_FILE = token2
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 
        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) 
        spreadsheetId ="19scZBB6xfrO5OV3Q-JzF5AZP1WFWPSxmcEA7zn6T-ps"
                #
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ["Аккаунты!A1:B2"], 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        try:
            sh=int(sheet_values[0][0])
        except:
            sh=1200
        ln253=max(sh+400,1600)
        ranges = ["Аккаунты!B3:J"+str(max(len(bot.accs)+40,ln253))] # 
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ranges, 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
                
        names=[]
        dg=[]
                
        ngmf=0

        for arr in sheet_values:
            if arr!=[]:
                names.append(arr[0])
                while len(arr)<9:
                    arr.append('')
                acc=bot.accs.get(arr[0],{'QR': '','Входы':{}})
                if arr[-1]!='':
                    tcheck, tmax=bot.parse_timestamp_to_unixtime(arr[-1])
                    if tcheck and tmax not in mtimes:
                        mtimes.append(tmax)
                        acc=bot.accs.get(arr[0],{'QR': '','Входы':{}})
                        vhs=0
                        for key in acc['Входы']:
                            vhs+=acc['Входы'][key]
                        mkey=str(int(tmax/60/60/24))
                        if mkey not in acc['Входы']: acc['Входы'][mkey]=0
                        acc['Входы'][mkey]+=1

                                
                        caption=f"[MMax] Обнаружен вход в аккаунт {arr[0]}\nВремя входа: {arr[-1]}\nБыло входов: {vhs}\nСтало входов: {vhs+1}\nСпасибо, Макс"
                        bot.my_bot.send_message(for_reports,caption)
                        bot.my_bot.send_message('832182441',caption)

                        bot.accs[arr[0]]=acc.copy()
                        ngmf+=1
        if ngmf!=0:
            db=shelve.open(MAX_PLEASE_DATA_SHELVE)
            db["mtimes"]=mtimes
            db.close()
            bot.little_save_data()

    def convert_shelve_to_tsv(self, shelve_path: str = AU_CODE_HAND_DATA_SHELVE) -> str:
        tsv_lines = []
        try:
            with shelve.open(AU_CODE_DATA_SHELVE, 'r') as db:
                for key, secret in db.items():
                    name = str(key).replace('\t', ' ').replace('\n', ' ')
                    secret_value = str(secret).replace('\t', ' ').replace('\n', ' ')
                    tsv_line = f"{name}\t{secret_value}"
                    tsv_lines.append(tsv_line)
                    
        except Exception as e:
            print(f"❌ Ошибка при чтении shelve файла {shelve_path}: {e}")
            return ""
        try:
            with shelve.open(shelve_path, 'r') as db:
                for key, secret in db.items():
                    name = str(key).replace('\t', ' ').replace('\n', ' ')
                    secret_value = str(secret).replace('\t', ' ').replace('\n', ' ')
                    tsv_line = f"{name}\t{secret_value}"
                    tsv_lines.append(tsv_line)
                    
        except Exception as e:
            print(f"❌ Ошибка при чтении shelve файла {shelve_path}: {e}")
            return ""
        
        tsv_data = "\n".join(tsv_lines)
        
        return tsv_data

    def convert_shelve_to_aegis_json(self,shelve_path: str = AU_CODE_HAND_DATA_SHELVE) -> Dict[str, Any]:
        entries = []
        
        try:
            with shelve.open(shelve_path, 'r') as db:
                for key, secret in db.items():
                    entry = {
                        "type": "totp",
                        "uuid": str(uuid.uuid4()),  
                        "name": str(key),  
                        "issuer": "",  
                        "note": "",
                        "favorite": False,
                        "icon": None,
                        "info": {
                            "secret": str(secret),
                            "algo": "SHA1",
                            "digits": 6,
                            "period": 30
                        },
                        "groups": []
                    }
                    entries.append(entry)
        
        except Exception as e:
            print(f"❌ Ошибка при чтении shelve файла {shelve_path}: {e}")
            return {}
        
        aegis_data = {
            "version": 1,
            "header": {
                "slots": None,
                "params": None
            },
            "db": {
                "version": 3,
                "entries": entries
            }
        }
        
        return aegis_data

    def reload(self,message=None):
        self.ams_sync()
        return 0
        bot.my_bot.send_message(for_reports,'reply: было аккаунтов '+str(len(bot.accs)))
        mail='https://console.developers.google.com/cloud-resource-manager'
        token2=GOOGLE_TOKEN
        CREDENTIALS_FILE = token2
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http()) 
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 
        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) 
        spreadsheetId ="19scZBB6xfrO5OV3Q-JzF5AZP1WFWPSxmcEA7zn6T-ps"
                #
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ["Аккаунты!A1:B2"], 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
        try:
            sh=int(sheet_values[0][0])
        except:
            sh=1200
        ln253=max(sh+400,1600)
        bot.my_bot.send_message(for_reports,'reply: выбранный максимум '+str(ln253)+'; введенное число '+str(sh))
        ranges = ["Аккаунты!B3:I"+str(max(len(bot.accs)+40,ln253))] # 
                          
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                     ranges = ranges, 
                                                     valueRenderOption = 'FORMATTED_VALUE',  
                                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values']
                
        names=[]
        dg=[]
                
                

        for arr in sheet_values:
            if arr!=[]:
                names.append(arr[0])
                while len(arr)<8:
                    arr.append('')
                acc=bot.accs.get(arr[0],{'QR': '','Входы':{}})
                acc['Пароль']=arr[1]
                acc['Почта']=arr[2]
                acc['Игры']=arr[4]
                acc['Дополнительно']=arr[3]
                acc['Резервные коды']=arr[7]
                        
                bot.accs[arr[0]]=acc.copy()
        for key in bot.accs:
            if key not in names: bot.my_bot.send_message(for_reports,'delete '+key+'\n'+str(bot.accs[key]));dg.append(key)
        for key in dg:
            bot.accs.pop(key)
                
        bot.my_bot.send_message(for_reports,'reply: стало аккаунтов '+str(len(bot.accs)))

        bot.little_save_data()
        bot.my_bot.send_message(for_reports,'reply: стало-2 аккаунтов '+str(len(bot.accs)))
        if message is not None:
            bot.my_bot.send_message(message.from_user.id,'Данные успешно обновлены', reply_markup=markup)

    def check_mail(self):
        try_task = []
        new_mail = ''
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        
        creds = None
        if os.path.exists(GOOGLE_REAL_TOKEN):
            creds = Credentials.from_authorized_user_file(GOOGLE_REAL_TOKEN, SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDS, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(GOOGLE_REAL_TOKEN, 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=60).execute()
        messages = results.get('messages', [])
        gmail_emails = []

        if not messages:
            self.my_bot.send_message(for_reports, "📭 Gmail: Нет новых сообщений.")
            return try_task

        db = shelve.open(BOT_END_DATA_SHELVE)
        last_mail = db.get('last_mail', '')
        db.close()
        
        processed_count = 0
        skipped_count = 0

        for message in messages:
            msg_id = message["id"]
            if msg_id == last_mail: 
                break
            if new_mail == '': 
                new_mail = msg_id
                
            try:
                msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                headers = msg["payload"].get("headers", [])
                subject = "Без темы"
                sender = "Неизвестно"
                for head in headers:
                    if head['name'] == 'Subject':
                        subject = head['value']
                    elif head['name'] == 'From':
                        sender = head['value']

                mtask = {'device': '', 'nick': '', 'mail': '', 'date': '', 'location': ''}
                coll = 0
                for head in headers:
                    if head['name'] == 'Date':
                        try:
                            dt = datetime.strptime(head['value'], "%a, %d %b %Y %H:%M:%S %z")
                            dt = dt.astimezone(pytz.timezone('Europe/Moscow')).strftime("%d/%m/%Y %H:%M") + " (мск)"
                            mtask['date'] = dt
                        except:
                            pass
                    elif head['name'] == 'Subject':
                        if any(x in head['value'] for x in ['New sign-in', 'Новый вход', 'Nouvelle connexion']):
                            coll = 1
                    elif head['name'] == 'Delivered-To':
                        mtask['mail'] = head['value'].strip().strip('<>')
                        coll = 1  
                    
                    elif head['name'] == 'To' and not mtask['mail']:
                        if 'Hide My Email' in head['value']:
                            start_ind = head['value'].find('<')
                            end_ind = head['value'].find('@icloud.com')
                            if start_ind != -1 and end_ind != -1:
                                mtask['mail'] = head['value'][start_ind+1:end_ind+11]
                                coll = 1
                        else:
                            import re
                            match = re.search(r'[\w\.-]+@[\w\.-]+', head['value'])
                            if match:
                                mtask['mail'] = match.group(0)
                                coll = 1

                if coll == 1:
                    try:
                        body_str = ""
                        if 'data' in msg['payload'].get('body', {}):
                            body_str = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('UTF-8', errors='ignore')
                        elif 'parts' in msg['payload']:
                            for part in msg['payload']['parts']:
                                if part.get('mimeType') in ['text/plain', 'text/html'] and 'data' in part.get('body', {}):
                                    body_str = base64.urlsafe_b64decode(part['body']['data']).decode('UTF-8', errors='ignore')
                                    break
                        
                        for keyword in ['Nickname', 'Ник', 'Surnom']:
                            if keyword in body_str:
                                start_ind = body_str.find(keyword)
                                end_ind = body_str.find('<br />', start_ind)
                                if end_ind == -1: end_ind = body_str.find('\n', start_ind)
                                if end_ind != -1: mtask['nick'] = body_str[start_ind:end_ind].strip()
                                break
                                
                        for keyword in ['Device', 'Устройство', 'Appareil']:
                            if keyword in body_str:
                                start_ind = body_str.find(keyword)
                                end_ind = body_str.find('<br />', start_ind)
                                if end_ind == -1: end_ind = body_str.find('\n', start_ind)
                                if end_ind != -1: mtask['device'] = body_str[start_ind:end_ind].strip()
                                break

                        if 'Forwarded to' in body_str:
                            start_ind = body_str.find('Forwarded to')
                            end_ind_net = body_str.find('@pxdmail.net', start_ind)
                            end_ind_com = body_str.find('@pxdmail.com', start_ind)
                            end_ind = end_ind_net if end_ind_net != -1 else end_ind_com
                            if end_ind != -1:
                                subst = body_str[start_ind:end_ind+12]
                                mtask['mail'] = subst.split('>')[-1].strip() if '>' in subst else subst.strip()

                        try_task.append(mtask)
                    except Exception as e:
                        self.my_bot.send_message(for_reports, f"⚠️ Ошибка парсинга Nintendo-входа {msg_id}: {e}")

                body_text = "[Пустое тело или не удалось извлечь]"
                try:
                    if 'parts' in msg['payload']:
                        for part in msg['payload']['parts']:
                            if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                                body_text = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                                break
                        else:
                            for part in msg['payload']['parts']:
                                if part.get('mimeType') == 'text/html' and 'data' in part.get('body', {}):
                                    html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                                    body_text = self.clean_html_to_text(html)
                                    break
                    else:
                        if 'data' in msg['payload'].get('body', {}):
                            body_text = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8', errors='ignore')
                except Exception as e:
                    body_text = f"[Ошибка чтения тела: {str(e)[:50]}...]"
                
                body_text = self.clean_html_to_text(body_text)
                
                final_recipient = mtask['mail'] if mtask['mail'] else "Не определен"
                
                gmail_emails.append({
                    'sender': sender,
                    'recipient': final_recipient, 
                    'subject': subject,
                    'body': body_text,
                    'received_at': datetime.now(pytz.UTC).isoformat()
                })
                processed_count += 1

            except Exception as e:
                skipped_count += 1
                error_msg = f"❌ Пропущено письмо {msg_id}\nТема: {subject}\nОт: {sender}\nОшибка: {str(e)[:100]}"
                self.my_bot.send_message(for_reports, error_msg)
                continue

        if new_mail != '':
            db = shelve.open(BOT_END_DATA_SHELVE)
            db['last_mail'] = new_mail
            db.close()

        
        if gmail_emails:
            self._send_emails_to_api(gmail_emails)
        
        return try_task


    def _send_emails_to_api(self, emails: list):
        if not emails:
            return
        
        url = f"{MAIL_API_BASE_URL}/api/emails/add/"
        headers = {
            'X-API-Key': MAIL_API_KEY,
            'Content-Type': 'application/json'
        }
        payload = {
            'emails': emails
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=MAIL_API_TIMEOUT
            )
            
            if response.status_code in (200, 207):
                try:
                    result = response.json()
                    created = result.get('created_count', 0)
                    errors = result.get('errors', [])
                    
                    if created > 0:
                        msg = f"📬 API: сохранено {created} писем в агрегатор"
                        if errors:
                            msg += f", {len(errors)} с ошибками"
                    
                    if errors:
                        for err in errors[:3]: 
                            idx = err.get('index', '?')
                            error = err.get('error', 'Unknown')
                        
                except ValueError:
                    pass
            
            elif response.status_code == 400:
                try:
                    err_data = response.json()
                    error_msg = err_data.get('error', 'Validation failed')
                    errors_detail = err_data.get('errors', [])
                    
                    msg = f"❌ API: ошибка валидации - {error_msg}"
                    if errors_detail:
                        msg += f" ({len(errors_detail)} писем отклонено)"
                    self.my_bot.send_message(for_reports, msg)
                    
                except ValueError:
                    self.my_bot.send_message(
                        for_reports,
                        f"❌ API: ошибка 400 - {response.text[:100]}"
                    )
            
            elif response.status_code == 401:
                self.my_bot.send_message(
                    for_reports,
                    "❌ API: неверный API-ключ (401 Unauthorized)"
                )
            
            elif response.status_code >= 500:
                self.my_bot.send_message(
                    for_reports,
                    f"⚠️ API: ошибка сервера ({response.status_code}). Письма не сохранены в агрегатор."
                )
            
            else:
                self.my_bot.send_message(
                    for_reports,
                    f"⚠️ API: неожиданный статус {response.status_code}"
                )
        
        except requests.exceptions.Timeout:
            self.my_bot.send_message(
                for_reports,
                f"⚠️ API: таймаут ({MAIL_API_TIMEOUT}с). Письма не сохранены в агрегатор."
            )
        
        except requests.exceptions.ConnectionError:
            self.my_bot.send_message(
                for_reports,
                "⚠️ API: не удалось подключиться к агрегатору. Письма не сохранены."
            )
        
        except Exception as e:
            self.my_bot.send_message(
                for_reports,
                f"⚠️ API: непредвиденная ошибка - {str(e)[:100]}"
            )

    def clean_html_to_text(self, html_content):
        """Превращает грязный HTML в чистый читаемый текст с сохранением ссылок"""
        import re
        
        if not html_content:
            return ""
            
        text = html_content
        
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        def replace_link(match):
            url = match.group(1).strip()
            link_text = match.group(2).strip()
            
            clean_text = re.sub(r'<[^>]+>', '', link_text).strip()
            
            if not clean_text:
                clean_text = "Ссылка"
                
            return f"{clean_text} ({url})"
            
        text = re.sub(
            r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', 
            replace_link, 
            text, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</tr>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</td>', ' ', text, flags=re.IGNORECASE)
        
        text = re.sub(r'<[^>]+>', '', text)
        
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        text = re.sub(r'\n\s*\n', '\n\n', text)  
        text = re.sub(r'[ \t]+', ' ', text)     
        text = text.strip()
        
        return text
    
        
    def give_your_password(self, name):
        byaka = False
        secret_key = ''
        login = 'Не найдено'
        
        shelve_files = [
            (AU_CODE_HAND_DATA_SHELVE, True),                 
            (AU_CODE_DATA_SHELVE, False)                    
        ]
        self.my_bot.send_message(for_reports,f"Ищем 2fa: {name}")
        for db_path, is_special_source in shelve_files:
                
            try:
                with shelve.open(db_path, flag='r') as db:
                    for acc in db:
                        accn = "".join([su for su in acc if su not in "()"])
                        if name == accn:
                            self.my_bot.send_message(for_reports,f"Найдено в точном списке: {db_path} - {accn}")
                            if login!='Не найдено':
                                secret_key = db[acc]
                                login = acc
                                if is_special_source:
                                    byaka = True  
            except Exception:
                pass
        
        for db_path, is_special_source in shelve_files:
            try:
                with shelve.open(db_path, flag='r') as db:
                    for acc in db:
                        accn = "".join([su for su in acc if su not in "()"])
                        if name in accn.split() or name in accn:
                            self.my_bot.send_message(for_reports,f"Найдено в почтишном списке: {db_path} - {accn}")
                            if login!='Не найдено':
                                secret_key = db[acc]
                                login = acc
                                if is_special_source:
                                    byaka = True  
            except Exception:
                pass
        if secret_key != '':
            try:
                totp = pyotp.TOTP(secret_key)
                secret_key = totp.now()
            except Exception as e:
                login = f"Ошибка генерации: {str(e)}"
                secret_key = ''
                
        return login, secret_key, byaka



    def create_button(self):
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить аккаунт")
        btn2_1 = types.KeyboardButton("/reload")
        btn2_2 = types.KeyboardButton("Поиск игры")
        btn5 = types.KeyboardButton("Дай почту")

        
        self.markup.add(btn1,btn2_1,btn2_2,btn5)
        
        self.markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Добавить аккаунт")
        btn2_1 = types.KeyboardButton("/reload")
        btn2_2 = types.KeyboardButton("Поиск игры")
        btn5 = types.KeyboardButton("Дай почту")
        self.markup2.add(btn1,btn2_1,btn2_2,btn5)
        
    def get_mname(self,nm):
        try:
            if re.fullmatch(r'.*(.*).*',nm) or re.fullmatch(r'(.*).*',nm) :
                ind=nm.index(')')
                nm2=nm[ind+1:]
                if nm2[0]==' ': nm2=nm2[1:]
                return nm2
            else:
                return nm
        except Exception as e:
            return nm
    def clean_expired_bans(self):
        current_time = time.time()
        expired_users = [
            user_id for user_id, ban_until in bad_boys.items()
            if ban_until <= current_time
        ]
        
        for user_id in expired_users:
            del bad_boys[user_id]
            self.my_bot.send_message(for_reports,f"🔓 User {user_id} автоматически разбанен")
    def clean_expired_change(self,login):
        current_time = time.time()
        dg=[]
        tchange=self.users[str(login)].get("tchange",[])
        for i in range(len(tchange)):
            if current_time>= tchange[i]+3600:
                dg.append(i)
        for i in range(len(dg)):
            tchange.pop(dg[-1-i])
        self.users[str(login)]["tchange"]=tchange
    def add_new_change(self,login):
        current_time = time.time()
        tchange=self.users[str(login)].get("tchange",[])
        tchange.append(current_time)
        self.users[str(login)]["tchange"]=tchange
        if len(tchange)>=3 and str(login) not in bot.cool_boys:
            self.batya_report(f"Забанен на час из-за {len(tchange)} изменений данных аккаунтов в течение часа",login)
            bad_boys[str(login)]=current_time+3600
    def get_mmname(self,nm):
        try:
            if re.fullmatch(r'.*(.*).*',nm) or re.fullmatch(r'(.*).*',nm) :
                ind=nm.index(')')
                nm2=nm[ind+1:]
                if nm2[0]==' ': nm2=nm2[1:]
                nm2+='\nНомер: '
                ind2=nm.index('(')
                nm2+=nm[ind2+1:ind]
                return nm2
            else:
                return nm
        except Exception as e:
            return nm
            
        
            
    
    def au_list_admin(self,message):
        txt="Администраторы:\n"
        i=1
        for key in self.auth:
            txt+=str(i)+". "+key+": "+self.auth[key]+'\n'
            i+=1
        self.my_bot.send_message(message.from_user.id,txt)
        txt="Администраторы:\n"
        i=1
        for key in self.ids:
            txt+=str(i)+". "+key
            if key in self.auth:
                txt+=f" {self.auth[key]}"
            txt+='\n'
            i+=1
        self.my_bot.send_message(message.from_user.id,txt)
        
    def au_load_admin(self,message):
        db=shelve.open(ADMIN_DATA_SHELVE)
        self.auth=db.get('auth',auth)
        self.ids=db.get('ids',ids)
        db.close()
        txt="Администраторы:\n"
        for key in self.auth:
            txt+=self.auth[key]+'\n'
        self.my_bot.send_message(message.from_user.id,txt)
        self.my_bot.send_message(message.from_user.id,str(self.ids))

    def is_night_time(self):
        now = datetime.now().time()
        return datetime_time(22, 40) <= now or now <= datetime_time(6, 30)

    def batya_report(self,caption,user):
        username=self.auth.get(str(user),str(user))
        caption=f"Пользователь {username}: "+caption
        self.my_bot.send_message('832182441',caption)
        self.my_bot.send_message(for_reports,caption)
        
    def au_del_admin(self,message):
            self.users[str(message.from_user.id)]['route']='au_del_admin'
            self.my_bot.send_message(message.from_user.id,'Введите id администратору, которого хотите удалить или выберите команду отмены (/back). Для получения id перешлите любое его сообщение @getidsbot.')
    def au_del_admin2(self,message):
            txt=message.text
            
            if txt in self.ids:
                self.ids.pop(self.ids.index(txt))
            if txt in self.auth:
                self.auth.pop(txt)
            self.users[str(message.from_user.id)]['route']='start'
            self.my_bot.send_message(message.from_user.id,'Администратор удален')
            
            
            db=shelve.open(ADMIN_DATA_SHELVE)
            db['auth']=self.auth
            db['ids']=self.ids
            db.close()

    def adbot2_mail(self):

        try:
            results=bot.check_mail()


            db=shelve.open(BOT_END_DATA_SHELVE)
            table_vhods=db.get('table_vhods',{})
            table_vhods_double=db.get('table_vhods_double',{})
            db.close()
            mails={}
            mails_double={}
            for arr in results:
                txt2='Получено письмо:\n'
                txt_double=''
                for key in arr:
                    if arr[key]=='':
                        txt2+=key+' - '+'[не обнаружено]'+'\n'
                    else:
                        txt2+=key+' - '+arr[key]+'\n'
                    if key=='date' or key=='nick':
                        if arr[key]=='':
                            txt_double+=key+' - '+'[не обнаружено]'+'\n'
                        else:
                            txt_double+=key+' - '+arr[key]+'\n'

                if arr['mail']!='':
                    arr3332=mails.get(arr['mail'],[])
                    arr3332.insert(0,txt2)
                    mails[arr['mail']]=arr3332
                    arr3332=mails_double.get(arr['mail'],{})
                    arr3332[txt2]=txt_double
                    mails_double[arr['mail']]=arr3332
            for accname in bot.accs: 

                if bot.accs[accname]['Почта'] in mails:
                    for text_mail in mails[bot.accs[accname]['Почта']]:

                        check_in=mails_double[bot.accs[accname]['Почта']].get(text_mail,'-1')
                        if check_in=='-1' or check_in not in table_vhods_double.get(bot.accs[accname]['Почта'],[]):

                            if check_in!='-1':
                                arr34324235=table_vhods_double.get(bot.accs[accname]['Почта'],[])
                                arr34324235.append(check_in)
                                table_vhods_double[bot.accs[accname]['Почта']]=arr34324235
                                    
                            acc=bot.accs[accname]
                            key=str(bot.get_day())
                            key_vhod=accname+' _^_ '+key
                            a=0
                            b=0
                                    
                            for key2 in acc['Входы']:
                                if int(key)-int(key2)<=30:
                                    a+=acc['Входы'][key2]
                                b+=acc['Входы'][key2]
                            if 'Nintendo Switch' in text_mail:
                                cou46 = ' не отмечен (функция временно отключена)'
                                d2 = table_vhods.get(key_vhod, 0) + 1
                                table_vhods[key_vhod] = d2
                                if 1>2:
                                    try:
                                        ams_account_id = acc.get('ams_account_id', '')
                                        if not ams_account_id:
                                            email = acc.get('Почта', '')
                                            if email:
                                                ams_info = bot.ams.get_account_id_by_email(email)
                                                if ams_info.get("ok"):
                                                    ams_account_id = ams_info.get("accountId", "")
                                                    acc['ams_account_id'] = ams_account_id
                                        
                                        if ams_account_id:
                                            new_total = acc.get('loginsTotal', 0) + 1
                                            new_30d = acc.get('logins30d', 0) + 1
                                            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            
                                            patch_res = bot.ams.update_account(ams_account_id, {
                                                "loginsTotal": new_total,
                                                "logins30d": new_30d,
                                                "lastLogins": now_str,
                                                "reason": "Auto login detected from Nintendo email"
                                            })
                                            
                                            if patch_res.get("ok"):
                                                acc['loginsTotal'] = new_total
                                                acc['logins30d'] = new_30d
                                                acc['lastLogins'] = now_str
                                                bot.accs[accname] = acc
                                                cou46 = 'отмечен'
                                                a = new_30d
                                                b = new_total
                                            else:
                                                cou46 = f' не отмечен (AMS ошибка: {patch_res.get("error", "?")})'
                                        else:
                                            cou46 = ' не отмечен (AMS не найден)'
                                    except Exception as e:
                                        bot.my_bot.send_message(for_reports, f"⚠️ AMS отметка входа для {accname}: {traceback.format_exc()}")
                                        cou46 = ' не отмечен (исключение)'
                            emio=0
                            for idn in bot.users: 
                                try:
                                    txt3=''
                                    if "Linux" in text_mail:
                                        pass
                                    elif 'device - [не обнаружено]' in text_mail:
                                        if idn==for_reports:
                                                    
                                            txt3='\u203C️ '
                                            txt3+='Вход в аккаунт '+accname+'\n'+str(text_mail)
                                            bot.my_bot.send_message(idn,txt3)
                                    elif 'Nintendo Switch' not in text_mail:
                                        txt3='\u203C️ '
                                        txt3+='Вход в аккаунт '+accname+'\n'+str(text_mail)
                                        bot.my_bot.send_message(idn,txt3)
                                                
                                    else:
                                        if cou46=='отмечен':
                                            markupin=types.InlineKeyboardMarkup()
                                            markupin.add(types.InlineKeyboardButton('Отмена входа',callback_data='revhod45_'+key_vhod))
                                            txt3+='Вход в аккаунт '+accname+' '+cou46+' ('+str(a)+'/'+str(b)+')\n'+str(text_mail)
                                            bot.my_bot.send_message(idn,txt3, reply_markup=markupin)
                                except:
                                    pass
                                
                                    
                            mails[bot.accs[accname]['Почта']]=[]

                        else:
                            pass

            for mail in mails:
                if mails[mail]!=[]:
                    pass
                            
            db=shelve.open(BOT_END_DATA_SHELVE)
            db['table_vhods']=table_vhods
            db['table_vhods_double']=table_vhods_double
            db.close()

            
        except:
            print(traceback.format_exc())
            try:
                bot.my_bot.send_message(for_reports,'Почта стухла')
                bot.my_bot.send_message(for_reports,traceback.format_exc())

            except:
                pass
                
    def au_new_admin(self,message):
            self.users[str(message.from_user.id)]['route']='au_new_admin'
            self.my_bot.send_message(message.from_user.id,'Введите id пользователя, которого хотите сделать новым администратором или выберите команду отмены (/back). Для получения id перешлите любое его сообщение @getidsbot.')
    def au_new_admin2(self,message):
            txt=message.text
            self.users[str(message.from_user.id)]['cash']=txt
            self.users[str(message.from_user.id)]['route']='au_new_admin2'
            self.my_bot.send_message(message.from_user.id,'Введите имя нового администратора. Например, 👤 Николай (@tg_kolya)')

    def draw_page(self,arro,start,dlen,user):
        ind=0
        if len(arro)<start:
            bot.my_bot.send_message(user,"--- Это всё! ---")
            return
        
        arro2=arro[start:]
        time.sleep(0.8)
        if dlen==23:
            dlen=len(arro2)

        for a in arro2:
            ind+=1
            if ind>dlen:

                sts=f"Найдено еще {len(arro2)-dlen} аккаунтов. Продолжить?"
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Продолжить',callback_data='pagisosi_'+str(user)))
                if (len(arro2)-dlen)>20: markupin.add(types.InlineKeyboardButton('Показать всё',callback_data='pagisosimnogo_'+str(user)))
                markupin.add(types.InlineKeyboardButton('Отмена',callback_data='pagidie_'+str(user)))
                self.page[str(user)]=start+dlen
                bot.my_bot.send_message(user,sts, reply_markup=markupin)
                break

            
            try:
                acc=bot.accs[a[1]]
                aa, b = bot.get_vhody(acc)
                txt2=a[1]+' ('+str(aa)+'/'+str(b)+')\n\n'+a[0]
                        
                txt2+=bot.check_date(acc['Дополнительно'].lower())
                today = datetime.now().date()
                date_str = acc.get("Очищено","15.05.2020")
                other_date = datetime.strptime(date_str, "%d.%m.%Y").date()
                delta = today - other_date  
                delta = delta.days     
                if delta <=30:
                    txt2="🧹 Внимание! Входы очищались "+acc.get("Очищено","15.05.2020")+" ("+str(delta)+" дней назад)\n"+txt2
                if 'основа' in acc['Дополнительно'].lower():
                    txt2='⚠️ '+txt2
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Инфо',callback_data='info_'+a[1]+str('_')+str(user)))
                bot.my_bot.send_message(user,txt2, reply_markup=markupin)
                if dlen>20: time.sleep(random.randint(3,8)/10)
            except Exception as e:
                bot.my_bot.send_message(for_reports,traceback.format_exc())
                bot.imt(user,str(traceback.format_exc()))
        if ind<=dlen:
            bot.my_bot.send_message(user,"--- Это всё! ---")
                
    def au_new_admin3(self,message):
            txt=message.text
            idm=self.users[str(message.from_user.id)].get('cash','-1')
            if idm!='-1':
                self.ids.append(idm)
                self.auth[idm]=txt
                self.users[str(message.from_user.id)]['route']='start'
                self.my_bot.send_message(message.from_user.id,'Новый администратор успешно добавлен')
                
            
                db=shelve.open(ADMIN_DATA_SHELVE)
                db['auth']=self.auth
                db['ids']=self.ids
                db.close()
            else:
                self.routes[message.from_user.id]['route']='start'
                self.my_bot.send_message(message.from_user.id,'Ошибка ввода id администратора')
                
    def check_maks_tek(self):
        ACTIVATIONS_QUEUE_SIZE.set(len(bot.maks_tek))
        initial_count = len(bot.maks_tek)
        if initial_count == 0:
            return 
        bot.my_bot.send_message(for_reports, f"🔄 Начинаю проверку очереди. Всего задач: {initial_count}")
        
        dg = [] 
        report_lines = [] 
        
        for key in list(bot.maks_tek.keys()):  
            try:
                task = bot.maks_tek[key]
                task_id = key
                login_name = task.get("login", "Аккаунт")
                forwhy = task.get("forwhy", "Unknown")
                coding = task.get("coding", "unknown")
                
                status_result = api.get_nintendo_status(task_id)
                if status_result["status"] == "error":
                    error_code = status_result.get("error_code", "UnknownError")
                    api_message = status_result.get("message", "Неизвестная ошибка")
                    report_lines.append(
                        f"🔴 Задача `{task_id}` ({login_name}) для {forwhy}: "
                        f"Ошибка API - [{error_code}] {api_message}"
                    )
                    dg.append(key)
                    ACTIVATION_CHECKS_TOTAL.labels(final_status='api_error').inc()
                    
                    markupin = types.InlineKeyboardMarkup()
                    if "login" in task:
                        markupin.add(types.InlineKeyboardButton('Отправить код снова', callback_data=f'givemeyourpussy_{task["login"]}'))
                    
                    bot.my_bot.send_message(
                        task["user"],
                        f"❌ Ошибка проверки статуса: {api_message}",
                        reply_markup=markupin
                    )
                    
                    continue
                
                task_status = status_result.get("task_status")    
                final_code = status_result.get("final_code")     
                data = status_result.get("data", {}) or {}
                txt_status = data.get("TxtStatus", "")
                if status_result["status"] == "success" and final_code:
                    report_lines.append(f"🟢 Задача `{task_id}` ({login_name}): Успешно! Код: `{final_code}`")
                    
                    safe_login = escape_md_v2(str(login_name))
                    safe_user = escape_md_v2(str(task['user']))
                    safe_task_id = escape_md_v2(str(task_id))
                    safe_code = escape_md_v2(str(final_code))
                    
                    message_text = (
                        f"✅ Успешная активация для [{escape_md_v2(forwhy)}]({forwhy}) по задаче {safe_login}\n"
                        f"\n"
                        f"`📨 Введите код на консоли: {safe_code}`\n"
                        f"\n"
                        f"`📨 Enter the code on the console: {safe_code}`\n"
                        f"\n"
                        f"Dev: {safe_task_id}\n"
                    )
                    
                    try:
                        bot.my_bot.send_message(task["user"], message_text, parse_mode="MarkdownV2")
                    except Exception as e:
                        print(f"Ошибка отправки с Markdown: {e}")
                        bot.my_bot.send_message(task["user"], message_text)
                        bot.my_bot.send_message(for_reports, message_text)
                    
                    if "login" in task:
                        bot.suchim(
                            str(task["user"]),
                            f"Успешная выдача кода для {forwhy} ({task['login']}), код с консоли {coding}"
                        )
                    dg.append(key)
                    ACTIVATION_CHECKS_TOTAL.labels(final_status='success').inc()
                
                elif task_status == 4:
                    ext_status = data.get("ExtStatus", "") or ""
                    error_code = status_result.get("error_code", "")
                    
                    report_lines.append(
                        f"🔴 Задача для {forwhy} `{task_id}` ({login_name}): "
                        f"Неудача. Статус: {txt_status}, Ext: {ext_status}"
                    )
                    
                    dg.append(key)
                    ACTIVATION_CHECKS_TOTAL.labels(final_status='failed').inc()
                    
                    markupin = types.InlineKeyboardMarkup()
                    if "login" in task:
                        markupin.add(types.InlineKeyboardButton('Попробовать снова', callback_data=f'givemeyourpussy_{task["login"]}'))
                    
                    safe_forwhy_link = f"[{escape_md_v2(forwhy)}]({forwhy})"
                    safe_txt_status = escape_md_v2(str(txt_status))
                    safe_ext_status = escape_md_v2(str(ext_status or 'Нет деталей'))
                    
                    if "NintendoPasskeySignInRejected" in ext_status or "NintendoPasskeySignInRejected" in txt_status:
                        prv = (
                            f"❌ Активация для {safe_forwhy_link} не удалась\n"
                            f"Статус: {safe_txt_status}\n"
                            f"Детали: У аккаунта проблема с passKey, необходимо обратиться к технику или лиду направления"
                        )
                    
                    elif error_code == "CodeExpiredOrInvalid" or "CodeExpiredOrInvalid" in ext_status:
                        prv = (
                            f"❌ Активация для {safe_forwhy_link} не удалась\n"
                            f"Статус: {safe_txt_status}\n"
                            f"Детали: Код консоли устарел или неверен\n"
                            f"🔄 Запросите новый 8\\-символьный код с консоли и повторите активацию"
                        )
                    
                    elif error_code == "TaskNotFoundByUuid" or "TaskNotFoundByUuid" in ext_status:
                        prv = (
                            f"⚠️ Заявка `{safe_task_id}` не найдена на сервере\n"
                            f"Передайте задачу оператору для ручного поиска принятой заявки\n"
                            f"НЕ запускайте новую активацию этого аккаунта"
                        )
                        markupin = types.InlineKeyboardMarkup()
                    
                    elif error_code == "Superseded" or "SupersededByNewRequest" in ext_status:
                        prv = (
                            f"⚠️ Активация для {safe_forwhy_link} отменена\n"
                            f"Эта заявка была заменена более поздним запросом по тому же аккаунту"
                        )
                    
                    else:
                        prv = (
                            f"❌ Активация для {safe_forwhy_link} не удалась\n"
                            f"Статус: {safe_txt_status}\n"
                            f"Детали: `{safe_ext_status}`"
                        )
                    
                    try:
                        bot.my_bot.send_message(
                            task["user"],
                            prv,
                            reply_markup=markupin,
                            parse_mode="MarkdownV2"
                        )
                        bot.my_bot.send_message(for_reports, prv, parse_mode="MarkdownV2")
                    except Exception as e:
                        print(f"Ошибка отправки Markdown: {e}")
                        clean_prv = prv.replace('[', '').replace('](', '').replace(')', '')
                        bot.my_bot.send_message(task["user"], clean_prv, reply_markup=markupin)
                        bot.my_bot.send_message(for_reports, clean_prv)
                
                else:
                    status_text = "в очереди" if task_status == 1 else "в обработке"
                    report_lines.append(
                        f"🟡 Задача для {forwhy} `{task_id}` ({login_name}): {status_text}"
                    )
                    ACTIVATION_CHECKS_TOTAL.labels(final_status='pending').inc()
            
            except Exception as e:
                error_trace = traceback.format_exc()
                report_lines.append(f"⚠️ Задача `{key}`: Исключение - {str(e)}")
                bot.my_bot.send_message(for_reports, f"🚨 Критическая ошибка в check_maks_tek для {key}:\n{error_trace}")
        
        for key in dg:
            bot.maks_tek.pop(key)
            
        if dg:
            bot.little_save_data()  
            
        if report_lines:
            final_count = len(bot.maks_tek)
            header = f"📊 *Итоги проверки:* \nОсталось в очереди: {final_count}\n\n"
            footer = "\n_Конец отчета_"
            
            full_report = header + "\n".join(report_lines) + footer
            
            chunk_size = 3500
            for i in range(0, len(full_report), chunk_size):
                chunk = full_report[i:i + chunk_size]
                safe_chunk = escape_md_v2(chunk)
                bot.my_bot.send_message(for_reports, safe_chunk, parse_mode="MarkdownV2")
            
    def auth_save_data(self):

        db=shelve.open(ADMIN_DATA_SHELVE)
        db['people_admin']=self.people_admin
        db['people_hueplekalo']=self.people_hueplekalo
        db['cool_boys']=self.cool_boys
        db.close()
            
    def little_save_data(self):
        
        db=shelve.open(BOT_END_DATA_SHELVE)
        db['users']=self.users
        db['accs']=self.accs
        db['alarms4t']=self.alarms4t
        db["tegs"]=self.tegs
        db["maks_tek"]=self.maks_tek
        db.close()

    def save_data(self):
        db=shelve.open(BOT_END_DATA_SHELVE)
        db['users']=self.users
        db['accs']=self.accs
        self.my_bot.send_message(for_reports,"запись в дб и гугл: "+str(len(self.accs)))
        db['alarms4t']=self.alarms4t
        db["tegs"]=self.tegs
        db["maks_tek"]=self.maks_tek
        db.close()
        
        
        db=shelve.open(BOT_END_DATA_SHELVE)
        arro={}
        for key in db:
            arro[key]=db[key]
        db.close()
        file_path = BOT_END_DATA_SHELVE  

        if os.path.exists(file_path):  
            os.remove(file_path)      
        db=shelve.open(BOT_END_DATA_SHELVE)
        for key in arro:
            db[key]=arro[key]
        db.close()
        if os.path.exists(BOT_END_DATA_RESERV_SHELVE):  
            os.remove(BOT_END_DATA_RESERV_SHELVE)       
        db=shelve.open(BOT_END_DATA_RESERV_SHELVE)
        for key in arro:
            db[key]=arro[key]
        db.close()

    
        
    def give_teg(self,login):
        acc=self.accs[login]
        if "#" not in acc["Дополнительно"]:
            gms2=acc["Игры"].lower()
            if gms2.count('\n')<6:
                gms=""
                for su in gms2:
                    if su in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                        gms+=su
                for ngm2 in self.tegs:
                    ngm=""
                    for su in ngm2:
                        if su.lower() in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                            ngm+=su.lower()
                    if ngm in gms:
                        acc["Дополнительно"]+=" "+self.tegs[ngm2]
                        break

    def get_day(self):
        t=int(time.time()/60/60/24)
        return t
    def parse_timestamp_to_unixtime(self,timestamp_str):
        try:
            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            unix_timestamp = dt.timestamp()
            
            return True, unix_timestamp
            
        except ValueError as e:
            return False, f"Ошибка формата: {e}"
        except Exception as e:
            return False, f"Неожиданная ошибка: {e}"
        
    def imt(self,user,st):
        if "Too Many Requests" in st:
            arro=[
            "Брат, честно, я заебался....",
            "Может нахуй эти аккаунты? Перекурим?",
            
    "Бля, опять эти ебучие нинтендо-акки... Может, просто притворимся, что сервера легли?",  
    "Бля, ну вот честно — я бы лучше пол тёр, чем этим занимался. Давай забить болт?",  
    "Бля, ну вот реально — зачем напрягаться? Давай просто представим, что мы уже всё сделали!",  
    "Всё, я сдаюсь. Сегодня мой день ‘ничегонеделания’. Предлагаю поддержать традицию!",  
    "Бля, ну вот реально — давай просто потратим время на какую-то хуйню? А работу — потом. Может быть. Или нет.",
    "Бля, ну я ваще не в теме... Может, забить и сделать вид, что мы тут ни при чём?",
    "Чувак, я настолько в ахуе от этой хуйни, что готов просто лечь и прикинуться мёртвым...",
    "Брат, давай начистоту: я нихуя не хочу. Может, лучше в доту? Или просто поспим?",
    "Чел, я в режиме 'понедельника' — нихуя не работает, и мне норм. Давай оставим на завтра?",
    "Бро, мне кажется, мы слишком много пашем. Давай как в том меме: 'работа подождёт'?",
    "Бля, ну реально — кто вообще это придумал? Давай сольёмся, пока не поздно...",
    "Ой, да ладно, мы же не рабы. Давай просто потупим и скажем, что 'в процессе'.",
    "Слушай, а если мы просто... не будем? Ну вот вообще. Просто возьмём и не будем.",
    "Бля, ну я уже как загнанная лошадь... Точнее, как ленивая жопа. Давай отдохнём?",
    "Чувак, давай без напрягов — сегодня день 'хуй знает что'. Завтра разберёмся. Или нет.",
    "Всё, кина не будет. Я сегодня — это просто грустный смайлик. Давай не будем.",
    "Бро, давай как в детстве — сделаем вид, что нас нет. Работа сама сделается. Или нет. Ну и хуй с ней.",
    "Бля, ну сколько можно? Давай уже честно: мы оба знаем, что нихуя не сделаем. Может, признаемся?",
    "Всё, я сдаюсь. Сегодня не мой день. Завтра — тоже. Давай просто примем это?",

            ]
            st2=random.choice(arro)
            self.my_bot.send_message(user,st2)
    def escape_markdown_v2(self,text):
        escape_chars = '_*[]()~`>#+-=|{}.!'
        for char in escape_chars:
            text = text.replace(char, f'\\{char}')
        return text
    def suchim(self,bwho,bwhat):
        rp=[-1003507880815]
        for u in rp:
            try:
                uid=self.auth.get(bwho,"")
                mess=f"{uid} {bwho} {bwhat}"
                messi=f"[Осторожно! Менеджер работает] {mess}"
                self.my_bot.send_message(u,messi)
            except:
                pass
    def get_info(self,message,login,english):
        try:

            self.suchim(str(message.from_user.id),f"Искал аккаунт {login}")

            baccvu=self.users[str(message.from_user.id)].get("baccvu",[])
            baccvu.append(login)
            baccvu=self.users[str(message.from_user.id)]["baccvu"]=baccvu
            if login in self.errors_acc and time.time()-120*60<self.errors_acc[login]:
                self.my_bot.send_message(message.from_user.id, "Аккаунт помечен как ошибочный")
                return 0
            
            emoji_id = 5461099136461842504
            a=login
            acc=self.accs[login]
            txt=''
            today = datetime.now().date()
            date_str = acc.get("Очищено","15.05.2020")
            other_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            delta = today - other_date  
            delta = delta.days   
            if delta <=30:
                txt+="🧹 Внимание! Входы очищались "+acc.get("Очищено","15.05.2020")+" ("+str(delta)+" дней назад)\n"
                
            #
            lgh6=""
            lkj=""
            for su in login:
                if su not in "() ":
                    lkj+=su
            db=shelve.open(AU_CODE_HAND_DATA_SHELVE)
            for acc4 in db:
                accn=""
                for su in acc4:
                    if su not in "() ":
                        accn+=su
                if login in accn.split():
                    lgh6=acc4
                    break
            db.close()
            if lgh6!="":
                txt+=f"Для аккаунта {lgh6} загружен  отдельный QR с 2FA\n"

            ams_acc = self.ams_get_acc_by_login(login)
            if ams_acc:
                b = ams_acc.get('logins30d', 0)
                c = ams_acc.get('loginsTotal', 0)
                last_login = ams_acc.get('lastLogins', '-')
            else:
                key = str(self.get_day())
                b = 0
                c = 0
                for key2 in acc.get('Входы', {}):
                    if int(key) - int(key2) <= 30:
                        b += acc['Входы'][key2]
                    c += acc['Входы'][key2]
            
            
            txt+='Логин: '
            txt+=self.get_mmname(login)+'\n'
            txt+='Пароль: '
            txt+=acc['Пароль']+'\n'
            txt+='Почта: '
            txt+=acc['Почта']+'\n\n'
            txt+='Игры:\n'
            txt+=str(acc['Игры'])+'\n\n'
            txt+='Входы за последние 30 дней: '+str(b)+'\n'
            txt+='Всего входов: '+str(c)+'\n'

            if 'Дата рождения' in acc: txt+='Дата рождения: '+acc['Дата рождения']+'\n'

            txt+=self.check_date(acc['Дополнительно'].lower())
            if 'основа' in acc['Дополнительно'].lower():
                txt+='⚠️Дополнительно: '
            else:
                txt+='Дополнительно: '
            txt+=acc['Дополнительно']+'\n\n'
            if message.from_user.id in bot.people_admin+bot.people_hueplekalo:
                txt+='Резервные коды: '+'\n'
                txt+=str(acc.get('Резервные коды',""))+'\n'
            bi2=self.alarms4t.get(a,[])
            if bi2!=[]:
                txt+='Аккаунт сдан в аренду; аренда истекает через '+str( (bi2[1]-time.time())/60/60//24 )+' дней\n'
            if english:
                
                if "яндекскака" in acc['Дополнительно'].lower():
                    txt='\u200B'+txt
                    emoji_entity = types.MessageEntity(
                        type='custom_emoji',
                        offset=0, 
                        length=1,   
                        custom_emoji_id=emoji_id
                    )
                    self.my_bot.send_message(message.from_user.id,txt,entities=[emoji_entity])
                else:
                    self.my_bot.send_message(message.from_user.id,txt)
            fnm=a
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Получить код 2FA',callback_data='2fa_'+fnm))
            markupin.add(types.InlineKeyboardButton('Отметить вход',callback_data='vhod_'+fnm))
            markupin.add(types.InlineKeyboardButton('Выдать аккаунт',callback_data='givemeyourpussy_'+fnm))
            markupin.add(types.InlineKeyboardButton('Отменить последний вход',callback_data='delvhod_'+fnm))
            markupin.add(types.InlineKeyboardButton('Очистить входы',callback_data='clearvh_'+fnm))
            markupin.add(types.InlineKeyboardButton('Инфо',callback_data='info_'+fnm+str('_')+str(message.from_user.id)))
            markupin.add(types.InlineKeyboardButton('Изменить данные',callback_data='folderchange_'+fnm))
            markupin.add(types.InlineKeyboardButton('Удалить аккаунт',callback_data='del_'+fnm))
            
            txt578='Сделать подписочным'
            if acc.get('trade',False): txt578='Убрать из подписки'
            txt=''
            
            today = datetime.now().date()
            date_str = acc.get("Очищено","15.05.2020")
            other_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            delta = today - other_date 
            delta = delta.days     
            if delta <=30:
                txt+="🧹 Внимание! Входы очищались "+acc.get("Очищено","15.05.2020")+" ("+str(delta)+" дней назад)\n"

            #
            
            txt+=self.check_date(acc['Дополнительно'].lower())
            if 'основа' in acc['Дополнительно'].lower():
                txt='⚠️\n'

            
            txt33=txt
            txtd33='Login: '+bot.get_mname(fnm)+'\n'
            txtd33+='Password: '
            txtd33+=acc['Пароль']
            txtd='Логин: '+bot.get_mname(fnm)+'\n'
            txtd+='Пароль: '
            txtd+=acc['Пароль']+'\n'
            
            try:
                if "яндекскака" in acc['Дополнительно'].lower():
                    txt33='\u200B'+txt33
                    emoji_entity = types.MessageEntity(
                        type='custom_emoji',
                        offset=0,  
                        length=1,  
                        custom_emoji_id=emoji_id
                    )
                    self.my_bot.send_message(message.from_user.id,self.escape_markdown_v2(txt33)+'```Credentials:\n'+self.escape_markdown_v2(txtd33)+'```', parse_mode='MarkdownV2',entities=[emoji_entity])
                else:
                    self.my_bot.send_message(message.from_user.id,self.escape_markdown_v2(txt33)+'```Credentials:\n'+self.escape_markdown_v2(txtd33)+'```', parse_mode='MarkdownV2')
            except:
                pass
            if "яндекскака" in acc['Дополнительно'].lower():

                stickers = self.my_bot.get_custom_emoji_stickers([str(emoji_id)])
                print('stickers',stickers)

                txtu='2\u200B'
                emoji_entity = types.MessageEntity(
                        type='custom_emoji',
                        offset=1,  
                        length=1,  
                        custom_emoji_id=str(emoji_id)
                    )
                self.my_bot.send_message(message.from_user.id,txtu, entities=[emoji_entity])
                self.my_bot.send_message(message.from_user.id,txt+txtd, reply_markup=markupin)
            else:
                self.my_bot.send_message(message.from_user.id,self.escape_markdown_v2(txt)+'```Данные:\n'+self.escape_markdown_v2(txtd)+'```', reply_markup=markupin, parse_mode='MarkdownV2')
            try:
                self.my_bot.send_photo(message.from_user.id,acc['QR'])
            except:
                pass
        except Exception as e:
            self.my_bot.send_message(for_reports,traceback.format_exc())
            self.imt(message.from_user.id,str(traceback.format_exc()))
            debag(traceback.format_exc())
bot=Bot()
api = CyndykShopAPI_key  


@bot.my_bot.message_handler(content_types=['photo'])
def get_photo(message):
    
        if str(message.from_user.id) in bad_boys:
            bot.my_bot.send_message(message.from_user.id,'Я сплю')
        elif bot.is_night_time() and str(message.from_user.id) not in bot.cool_boys:
            bot.my_bot.send_message(message.from_user.id,'Я сплю')
        elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#3':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
            markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
         
           
            htxt=message.photo[0].file_id
            bot.users[str(message.from_user.id)]['data_acc#3']=htxt
            bot.users[str(message.from_user.id)]['route']='add_acc#4'
            bot.my_bot.send_message(message.from_user.id,'QR код сохранен. Введите адрес почты.', reply_markup=markupin)
        elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#3':
            #
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='reaccept_'+str(message.from_user.id)))
            markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
            #
            acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
            markup=bot.markup
            htxt=message.photo[0].file_id
            bot.users[str(message.from_user.id)]['data_acc#3']=htxt
            bot.users[str(message.from_user.id)]['route']='change_acc#4'
            login=str(message.from_user.id)
            bot.my_bot.send_message(message.from_user.id,'Пароль: '+acc['Пароль']+' -> '+bot.users[login]['data_acc#0']+'\nПочта: '+acc['Почта']+' -> '+
                                        bot.users[login]['data_acc#0_1']+'\nИгры: '+acc['Игры']+' -> '+bot.users[login]['data_acc#1']+'\nРезервные коды: '+acc['Резервные коды']+' -> '+bot.users[login]['data_acc#1_1']+'\nДополнительно: '+
                                        acc['Дополнительно']+' -> '+bot.users[login]['data_acc#2']+'\nПодтвердите изменение данных', reply_markup=markupin)
        elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='send_qr_2fa':
            
            bot.users[str(message.from_user.id)]['route']=''
            
            try:
                file_info = bot.my_bot.get_file(message.photo[-1].file_id)
                downloaded_file = bot.my_bot.download_file(file_info.file_path)
                img_path = 'temp_qr.jpg'
                with open(img_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                img = cv2.imread(img_path)
                decoded_objects = decode(img)

                if decoded_objects:
                    for obj in decoded_objects:
                        qr_data = obj.data.decode('utf-8')
                        try:
                            st=str(qr_data)
                            st11=bot.users[str(message.from_user.id)]['set_acc']
                            st2=st[st.find('secret=')+7:]
                            st2=st2[:st2.find('&')]
                            db=shelve.open(AU_CODE_DATA_SHELVE)
                            if st11 in db:
                                bot.my_bot.reply_to(message, f"Код успешно обновлен для записи {st11}")
                                db[st11]=st2
                            else:
                                bot.my_bot.reply_to(message, f"Создана новая запись: {st11}")
                                db[st11]=st2
                            db.close()
                            
                            db=shelve.open(AU_CODE_HAND_DATA_SHELVE)
                            db[st11]=st2
                            db.close()
                        except:
                            bot.my_bot.reply_to(message, f"QR-код распознан, но возникла ошибка при форматировании: {qr_data}")
                            bot.my_bot.send_message(for_reports,traceback.format_exc())
                            debag(traceback.format_exc())
                else:
                    bot.my_bot.reply_to(message, "Не удалось распознать QR-код. Убедитесь, что фото четкое.")
                os.remove(img_path)

            except Exception as e:
                bot.my_bot.reply_to(message, f"Произошла ошибка: {e}")
                bot.my_bot.send_message(for_reports,traceback.format_exc())
                debag(traceback.format_exc())

        
 
@bot.my_bot.message_handler(commands=['test_ams'])
def test_ams(message):
    try:
        to_del = []
        for k, a in list(bot.accs.items()):
            if '@' in k and a.get('Пароль')=="***":  
                to_del.append(k)
        for k in to_del:
            del bot.accs[k]
        bot.my_bot.send_message(message.from_user.id, f"Удалено {len(to_del)}")
        bot.my_bot.send_message(message.from_user.id, f"Осталось {len(bot.accs)}")
    except Exception as e:
        bot.my_bot.send_message(message.from_user.id, str(e))
    try:
        if not hasattr(bot, 'ams') or bot.ams is None:
            bot.my_bot.send_message(for_reports, "❌ /test_ams: Клиент AMS не инициализирован в __init__ (self.ams = None)")
            bot.my_bot.send_message(message.from_user.id, "❌ AMS не настроен")
            return
        
        if str(message.from_user.id) not in bot.ids:
            bot.my_bot.send_message(message.from_user.id, "🚫 Недостаточно прав")
            return

        bot.my_bot.send_message(message.from_user.id, "⏳ Запрашиваю список аккаунтов из AMS API...")

        result = bot.ams.get_accounts_list(include_disabled=False, limit=10)
        
        if not result.get("ok"):
            err_text = f"❌ AMS API вернул ошибку:\n{result}"
            bot.my_bot.send_message(for_reports, err_text)
            bot.my_bot.send_message(message.from_user.id, "Ошибка при запросе к AMS. Смотри for_reports.")
            return

        items = result.get("items", [])
        total = result.get("total", 0)

        if not items:
            bot.my_bot.send_message(for_reports, f"⚠️ AMS: Список аккаунтов пуст (total={total})")
            bot.my_bot.send_message(message.from_user.id, f"⚠️ Аккаунты не найдены. Всего в базе: {total}")
            return

        first_acc = items[0]
        account_id = first_acc.get("accountId")
        email = first_acc.get("email", "нет почты")

        info_lines = [
            f"🧪 <b>TEST AMS: Первый аккаунт</b>",
            f"📊 Всего в базе: <b>{total}</b>",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"🆔 <b>AccountID:</b> <code>{account_id}</code>",
            f"📧 <b>Email:</b> {email}",
            f"👤 <b>LoginID:</b> {first_acc.get('loginId', '-')}",
            f"🏷 <b>AccountCode:</b> {first_acc.get('accountCode', '-')}",
            f"🎂 <b>BirthDate:</b> {first_acc.get('birthDate', '-')}",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"🎮 <b>Игры ({len(first_acc.get('gameTitles', []))}):</b>",
            f"  {', '.join(first_acc.get('gameTitles', [])[:5]) or '-'}",
            f"🏷 <b>Теги:</b> {', '.join(first_acc.get('gameTags', [])) or '-'}",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"📈 <b>Входы (30д):</b> {first_acc.get('logins30d', 0)}",
            f"📈 <b>Входы (всего):</b> {first_acc.get('loginsTotal', 0)}",
            f"🔄 <b>Последний вход:</b> {first_acc.get('lastLogins', '-')}",
            f"📦 <b>Резервные коды:</b> {first_acc.get('reserveCodesCount', 0)}",
            f"⚙️ <b>Статус:</b> {first_acc.get('lifecycleStatus', '-')}",
            f"📝 <b>Доп. инфа:</b> {first_acc.get('additionalInfo', '-')[:200]}",
            f"━━━━━━━━━━━━━━━━━━━━",
            f"📅 <b>Обновлено:</b> {first_acc.get('updatedAtUtc', '-')}",
        ]

        full_text = "\n".join(info_lines)
        
        bot.my_bot.send_message(for_reports, full_text, parse_mode='HTML')
        
        bot.my_bot.send_message(
            message.from_user.id, 
            f"✅ Первый аккаунт (<code>{email}</code>) выгружен в for_reports.\nВсего в AMS: {total}", 
            parse_mode='HTML'
        )

        if account_id:
            usages_res = bot.ams.get_usage_history(account_id, limit=3)
            if usages_res.get("ok"):
                usages = usages_res.get("items", [])
                if usages:
                    u_text = f"📜 <b>История выдач ({len(usages)} из {usages_res.get('total', '?')}):</b>\n"
                    for u in usages[:3]:
                        u_text += f"  • {u.get('client', '-')} | {u.get('gameTitle', '-')} | {u.get('marketplace', '-')}\n"
                    bot.my_bot.send_message(for_reports, u_text, parse_mode='HTML')

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        bot.my_bot.send_message(for_reports, f"💥 Критическая ошибка в /test_ams:\n{err}")
        bot.my_bot.send_message(message.from_user.id, f"💥 Упало. Смотри for_reports")
  
      
@bot.my_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        if str(message.from_user.id) in bot.ids:
            if str(message.from_user.id) not in bot.users:
                bot.users[str(message.from_user.id)]={'route':'start'}
            bot.clean_expired_bans()
            markup=bot.markup
            route=bot.users[str(message.from_user.id)]['route']
            if str(message.from_user.id) in bot.ids: markup=bot.markup2

            if bot.is_night_time():
                for login in bot.users:
                    bot.users[login]["baccvu"]=[]
                    bot.users[login]["bvhs"]=[]
            


            if (str(message.from_user.id) in bad_boys  and str(message.from_user.id) not in  bot.cool_boys) or str(message.from_user.id) not in bot.ids:
                bot.my_bot.send_message(message.from_user.id,'Я сплю')
            elif bot.is_night_time() and str(message.from_user.id) not in bot.cool_boys:
                bot.my_bot.send_message(message.from_user.id,'Я сплю')
          
            elif message.text=='/adbot2_mail' and str(message.from_user.id) in bot.ids:
                bot.adbot2_mail()
                

            elif message.text=="/back" and bot.users[str(message.from_user.id)]['route']=='add_gm#0':
                if bot.users[str(message.from_user.id)]['route']=='add_gm#0':
                    bot.users[str(message.from_user.id)]['route']='settings_acc'
                    bot.my_bot.send_message(message.from_user.id,'Аккаунт: '+bot.users[str(message.from_user.id)]['a']+':\n   /delete_acc - для удаления\n\n   /change_acc - для изменения информации об аккаунте\n/add_game_acc - для добавления игры\n   /list_game_acc - для вывода списка игр\n   /press_acc - для отметки входа\n   /stat_acc - для вывода статистики по входам\n\n   /clear_acc - для очистки входов', reply_markup=markup)
                else:
                    bot.users[str(message.from_user.id)]['route']=''
                    bot.my_bot.send_message(message.from_user.id,'А здесь приветственное сообщение', reply_markup=markup)
            elif message.text=='/save':
                bot.save_data()
                bot.my_bot.send_message(message.from_user.id,'Данные успешно обновлены', reply_markup=markup)
            elif message.text=='/back':
                bot.users[str(message.from_user.id)]['route']=''

            elif message.text=='/break':
                bot.users[str(message.from_user.id)]['route']=''
                try:
                    with open(DANCEDANCE_VIDEO, 'rb') as video_file:
                        bot.my_bot.send_video(
                            chat_id=message.chat.id,
                            video=video_file,
                            caption='Вы применили команду БРЕЙК!',  
                            supports_streaming=True  
                        )
                except Exception as e:
                    bot.my_bot.reply_to(message, f"Ошибка при отправке видео: {e}")



            
            elif message.text=='/max_sorry':
                mail='https://console.developers.google.com/cloud-resource-manager'
                token2= GOOGLE_TOKEN
                CREDENTIALS_FILE = token2
                credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
                httpAuth = credentials.authorize(httplib2.Http()) 
                service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)  
                driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) 
                spreadsheetId ="19scZBB6xfrO5OV3Q-JzF5AZP1WFWPSxmcEA7zn6T-ps"
                
                results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                                            ranges = ["Аккаунты!A1:B2"], 
                                                            valueRenderOption = 'FORMATTED_VALUE',  
                                                            dateTimeRenderOption = 'FORMATTED_STRING').execute() 
                sheet_values = results['valueRanges'][0]['values']
                sheet_values[0][0]=1000
                ln253=max(int(sheet_values[0][0])+17,len(self.accs)+20)
                ln253=max(ln253,1600)
                pvalues=[['']]
                for i in range(ln253):
                    pvalues.append([''])
                
                values.insert(0,   ["Логин", "Пароль", "Почта","Дополнительно","Игры","Входов за 30 дней","Входов всего",'Резервные коды'])
                results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                    "valueInputOption": "USER_ENTERED", 
                    "data": [
                    {"range": "Аккаунты!J1:J"+str(ln253+16),
                    "majorDimension": "ROWS",     
                    "values": pvalues}
                ]}).execute()
                db=shelve.open(MAX_PLEASE_DATA_SHELVE)
                db["mtimes"]=[]
                db.close()

            
            elif message.text=='/max_please':
                bot.max_please()

                

            elif message.text=='/reload' and str(message.from_user.id) in ['832182441','5266773307','741641254']:
                bot.reload()
            
            elif message.text=='/reload':
                bot.my_bot.send_message(message.from_user.id,"Вы недостойны")
                
            elif message.text=='/list_bad_boys' and message.from_user.id in bot.people_admin:
                txt="Список плохих мальчиков:\n"
                for key in bad_boys:
                    name=""
                    if str(key) in bot.auth:
                        name=f"{bot.auth[str(key)]} "
                    txt+=f"{name} {key}\n"
                bot.my_bot.send_message(message.from_user.id,txt)
                
            elif '/del_bad_boys' in message.text and message.from_user.id in bot.people_admin:
                try:
                    idn=message.text.split()[1]
                    del bad_boys[idn]
                    if idn not in bot.cool_boys: bot.cool_boys.append(idn)
                    bot.auth_save_data()
                    bot.my_bot.send_message(message.from_user.id,"Вы смогли")
                except:
                    bot.my_bot.send_message(message.from_user.id,"Вы не смогли")
                
            elif message.text=="Добавить аккаунт":
                markupin=types.InlineKeyboardMarkup()
               
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                bot.users[str(message.from_user.id)]['route']='add_acc#0'
                bot.my_bot.send_message(message.from_user.id,'Введите название нового аккаунта', reply_markup=markupin)
            elif message.text=="Вывести аккаунты":
                bot.users[str(message.from_user.id)]['route']=''
                txt=''
                
                for a in bot.accs:
                    acc=bot.accs[a]
                    b, c = bot.get_vhody(acc)
                    txt+=a+': '+acc.get('Пароль','***')+' (пароль), '+acc.get('Почта','')+'. Игр: '+str(len(acc.get('Игры','')))+'. Входы: ('+str(b)+'/'+str(c)+'). Дополнительно:'+acc.get('Дополнительно','')+' --> /settings_'+a+'\n'
                bot.my_bot.send_message(message.from_user.id,txt, reply_markup=markup)
            elif '/settings_' in message.text:
                a=message.text[10:]
                try:
                    at=bot.accs[a]
                    bot.users[str(message.from_user.id)]['a']=a
                    bot.users[str(message.from_user.id)]['route']='settings_acc'
                    bot.my_bot.send_message(message.from_user.id,'Аккаунт: '+a+':\n   /delete_acc - для удаления\n\n   /change_acc - для изменения информации об аккаунте\n/add_game_acc - для добавления игры\n   /list_game_acc - для вывода списка игр\n   /press_acc - для отметки входа\n   /stat_acc - для вывода статистики по входам\n\n   /clear_acc - для очистки входов', reply_markup=markup)
                except:
                    pass
            elif message.text=='Поиск игры':
                bot.users[str(message.from_user.id)]['route']='find_game'
                bot.my_bot.send_message(message.from_user.id,'Введите название игры', reply_markup=markup)

            elif message.text=="<Быстрые> команды":
                bot.users[str(message.from_user.id)]['route']=''
                arr1=['Используйте команды для быстрой отметки входа:\n']
                arr2=['Используйте команды для быстрого получения информации об акаунтах:\n']
                arr3=['Используйте команды для изменения информации об акаунтах:\n']
                for a in bot.accs:
                    acc=bot.accs[a]
                    arr1.append('/sign_'+a+' \n')
                    arr2.append('/check_'+a+' \n')
                    arr3.append('/change_'+a+' \n')
                    break
                txt=''
                cou=0
                for t in arr1:
                    cou+=1
                    txt+=t
                    if cou>=24:
                        cou=0
                        bot.my_bot.send_message(message.from_user.id,txt)
                        txt=''
                txt+='\n\n'
                for t in arr2:
                    cou+=1
                    txt+=t
                    if cou>=24:
                        cou=0
                        bot.my_bot.send_message(message.from_user.id,txt)
                        txt=''
                txt+='\n\n'
                for t in arr3:
                    cou+=1
                    txt+=t
                    if cou>=24:
                        cou=0
                        bot.my_bot.send_message(message.from_user.id,txt)
                        txt=''
                txt+='\nДля загрузки данных из Google таблицы: /reload'
                bot.my_bot.send_message(message.from_user.id,txt)
            elif '/sign_' in message.text:
                a=message.text[6:]
                try:
                    acc=bot.accs[a]
                    a2=a
                    key=str(bot.get_day())
                    d=acc['Входы'].get(key,0)+1
                    acc['Входы'][key]=d
                    bot.little_save_data()
                    a=0
                    b=0
                    for key2 in acc['Входы']:
                        if int(key)-int(key2)<=30:
                            a+=acc['Входы'][key2]
                        b+=acc['Входы'][key2]
                    bot.my_bot.send_message(message.from_user.id,'Вход в аккаунт '+а2+' #отмечен ('+str(a)+'/'+str(b)+')', reply_markup=markup)
                    if acc.get('trade',False):
                        bot.my_bot.send_message(message.from_user.id,'Введите ID консоли и ник покупателя')
                        bot.users[str(message.from_user.id)]['route']='add_id'
                        bot.users[str(message.from_user.id)]['a']=login
                        
                    
                except Exception as e:
                    bot.my_bot.send_message(for_reports,message.text)
                    bot.my_bot.send_message(for_reports,traceback.format_exc())
                    bot.imt(message.from_user.id,str(traceback.format_exc()))
                    debag(traceback.format_exc())
            elif "/secret_key" in message.text:
                bot.users[str(message.from_user.id)]['route']='gmyp'
                bot.my_bot.send_message(message.from_user.id,'Введите название или часть названия ключа')
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='gmyp':
                login,sc,byaka=bot.give_your_password(message.text)
                ss=int(time.time())%30
                ss=30-ss
                bot.my_bot.send_message(message.from_user.id,'Текущий код. До следующего кода: '+str(ss)+' сек.\nКод выдан для '+login)
                
                bot.my_bot.send_message(message.from_user.id,str(sc))
                bot.users[str(message.from_user.id)]['route']=''
            elif "/change_" in message.text:
                a=message.text[8:]
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                bot.users[str(message.from_user.id)]['a']=a
                acc=bot.accs[a]
                bot.users[str(message.from_user.id)]['route']='change_acc#0'
                bot.my_bot.send_message(message.from_user.id,'Текущий пароль: '+acc['Пароль']+'. Введите новый', reply_markup=markupin)
            elif message.text=="Главное меню":
                
                bot.my_bot.send_message(message.from_user.id,'Главное меню', reply_markup=markup)
            elif message.text=="Пользователи" and str(message.from_user.id) in bot.ids:
                sumarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn3 = types.KeyboardButton("Добавить пользователя")
                btn4 = types.KeyboardButton("Вывести пользователей")
                btn5 = types.KeyboardButton("Главное меню")
                sumarkup.add(btn3,btn4,btn5)
                bot.my_bot.send_message(message.from_user.id,'Пользователи', reply_markup=sumarkup)
            elif message.text=="Добавить пользователя" and str(message.from_user.id) in bot.ids:
                bot.users[str(message.from_user.id)]['route']='add_usr#0'
                bot.my_bot.send_message(message.from_user.id,'Введите ID нового пользователя (используйте @getidsbot) или выберите /back для отмены', reply_markup=markup)
            elif message.text=="Вывести пользователей" and str(message.from_user.id) in bot.ids:
                bot.users[str(message.from_user.id)]['route']=''
                txt=''
                for a in bot.users:
                    txt+=a+': '+bot.users[a]['name']+' /delete_acc_'+a+'\n'
                
                bot.my_bot.send_message(message.from_user.id,txt, reply_markup=markup)
            elif '/delete_acc_' in message.text and str(message.from_user.id) in bot.ids:
                a=message.text[12:]
                try:
                    bot.users.pop(a)
                    bot.little_save_data()
                    bot.my_bot.send_message(message.from_user.id,'Аккаунт удален', reply_markup=markup)
                except:
                    pass
            elif '/delete_game_' in message.text:
                a=message.text[13:]
                try:
                    bot.accs[bot.users[str(message.from_user.id)]['a']]['Игры'].pop(int(a))
                    bot.save_data()
                    bot.my_bot.send_message(message.from_user.id,'Игра удалена', reply_markup=markup)
                except Exception as e:
                    bot.my_bot.send_message(for_reports,message.text)
                    bot.my_bot.send_message(for_reports,traceback.format_exc())
                    bot.imt(message.from_user.id,str(traceback.format_exc()))
                    debag(traceback.format_exc())
            
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='find_game':
                bot.users.get(str(message.from_user.id),{'route':''})['route']=''
                txt=message.text
                arro=[]
                if ". основа" in txt:
                    ksgm=[]
                    for acc in bot.accs:
                        _, b = bot.get_vhody(bot.accs[acc]) 
                        ksgm.append([b, len(bot.accs[acc].get('Игры','')), acc])
                    ksgm.sort()
                    for acc in ksgm:
                        if 'основа' in bot.accs[acc[2]]['Дополнительно']:
                            games=bot.accs[acc[2]]['Игры']
                            arro.append([games,acc[2]])
                else:
                    main=False
                    solo=False
                    duo=False
                    hteg=""
                    if 'основа' in txt:
                        ind=txt.find("основа")
                        txt=txt[:ind]+txt[ind+6:]
                        main=True
                    if 'сольник' in txt:
                        ind=txt.find("сольник")
                        txt=txt[:ind]+txt[ind+7:]
                        solo=True
                    if 'сольнтк' in txt:
                        ind=txt.find("сольнтк")
                        txt=txt[:ind]+txt[ind+7:]
                        solo=True
                    if 'варианты' in txt:
                        ind=txt.find("варианты")
                        txt=txt[:ind]+txt[ind+len("варианты"):]
                        duo=True
                    for ttytxt in txt.split():
                        if "#" in ttytxt:
                            hteg=ttytxt



                    txt=txt.lower()
                    txt=txt.replace("\n",",")
                    txt=txt.split(',')
                    txt3=[]
                    txt_switch=[]

                    for t in txt:
                        if "switch 2 edition" in t:
                            ind=t.find("switch 2 edition")
                            txt3.append(t[:ind]+t[ind+len("switch 2 edition"):])
                            txt_switch.append(False)
                        elif "switch 2" in t:
                            ind=t.find("switch 2")
                            txt3.append(t[:ind]+t[ind+len("switch 2"):])
                            txt_switch.append(False)
                        else:
                            txt3.append(t)
                            txt_switch.append(True)
                    txt=txt3.copy()
                    txt3=[]
                    
                    for i in range(len(txt)):
                        t=txt[i]
                        
                        txt2=''
                        for su in t:
                            if su in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                                txt2+=su
                        if len(txt2)>1:
                            txt3.append(txt2)
                            
                    arro=[]
                    txt=txt3.copy()

                    
                    ksgm=[]
                    for acc in bot.accs:
                        _, b = bot.get_vhody(bot.accs[acc])  
                        ksgm.append([b, len(bot.accs[acc].get('Игры','')), acc])
                    ksgm.sort()
                    #
                    for acc in ksgm:
                        if ((main==False or 'основа' in bot.accs[acc[2]]['Дополнительно']) and solo==False) or (solo==True and 'основа' not in bot.accs[acc[2]]['Дополнительно'] and bot.accs[acc[2]]['Игры'].count('\n')<6) or (hteg!="" and hteg in bot.accs[acc[2]]['Дополнительно']):
                            games=bot.accs[acc[2]]['Игры']
                            
                            gm=games.lower().split("\n")
                            gm3=[]
                            for gm4 in gm:
                                gm2=''
                                for su in gm4:
                                    if su in '1234567890qwertyuiopasdfghjklzxcvbnm+':
                                        gm2+=su
                                gm3.append(gm2)
                            gm=gm3.copy()
                            coll=0
                            if duo:
                                cp=0
                                jkl=0
                                jij=0
                                for t in txt:
                                    jkl=0
                                    for ggm in gm:
                                        if t in ggm and t!='' and (txt_switch[jij] or "switch2" in ggm):
                                            if "mortalkombat11" not in txt[jij] and "mortalkombat" in txt[jij] and "mortalkombat11" in ggm:
                                                continue
                                            
                                            jkl+=1
                                    jij+=1
                                    if jkl>0:
                                        cp+=1
                                if cp>=2:
                                    coll=1
                            else:
                                coll=1
                                colli=[]
                                for ij in range(len(txt)):
                                    colli.append(0)
                                if len(txt)==0: coll=0
                                for ggm in gm:
                                    for iji in range(len(txt)):
                                        if txt[iji] in ggm and txt[iji]!='' and (txt_switch[iji] or "switch2" in ggm):
                                            if "mortalkombat11" not in txt[iji] and "mortalkombat" in txt[iji] and "mortalkombat11" in ggm:
                                                continue
                                            colli[iji]=1
                                if 0 in colli:
                                    coll=0
                            if acc[2] in bot.errors_acc and time.time()-120*60<bot.errors_acc[acc[2]]:
                                coll=0
                            if coll==1:
                                arro.append([games,acc[2]])
                                bot.give_teg(acc[2])
                            #

                    if len(arro)==0:
                        txt2='Игра не найдена'
                        bot.my_bot.send_message(message.from_user.id,txt2)
                    else:
                        txt2=f'Игра найдена на следующих аккаунтах ({len(arro)}):\n'
                        bot.my_bot.send_message(message.from_user.id,txt2)
                arromi=[]
                for a in arro:
                    _, b = bot.get_vhody(bot.accs[a[1]])
                    arromi.append([b, a]) 
                arromi.sort()

                arro2=[]
                for ab in arromi:
                    arro2.append(ab[1])

                bot.pagination[str(message.from_user.id)]=arro2
                bot.page[str(message.from_user.id)]=10

                bot.draw_page(arro2,0,10,message.from_user.id)


                
            
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#0':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                bot.users[str(message.from_user.id)]['data_acc#0']=message.text
                bot.users[str(message.from_user.id)]['route']='add_acc#1'
                bot.my_bot.send_message(message.from_user.id,'Название нового аккаунта сохранено. Введите пароль.', reply_markup=markupin)
                

            elif message.text=="/help_new_role_system" and str(message.from_user.id) in bot.ids:
                prv='''/help_new_role_system - помощь
/list_new_roles - вывести списки благословленных на работу с резервными кодами
/new_admin 123456 - добавить в админы пользователя с id 123456
/del_admin 123456 - удалить админа с id 123456
/new_rabotyaga 123456 - добавить в техники пользователя с id 123456
/del_rabotyaga 123456 - удалить техника с id 123456

/new_coolboys 123456 - добавить пользователя в белые списки
/del_coolboys 123456 - удалить пользователя из белых списков
/list_coolboys - показывает белые списки
'''
                bot.my_bot.send_message(message.from_user.id, prv)

            
            elif message.text=="/list_coolboys"  and str(message.from_user.id) in ["832182441","741641254","987177223","5266773307"]:
                prv=""

                prv+="Белые списки:\n"
                for key in bot.cool_boys:
                    name=""
                    if str(key) in bot.auth:
                        name=f"{bot.auth[str(key)]} "
                    prv+=f"{name} {key}\n"
                
                bot.my_bot.send_message(message.from_user.id, prv)

        

            elif "/new_coolboys" in message.text and str(message.from_user.id) in ["832182441","741641254","987177223","5266773307"]:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if str(abn[1]) not in bot.cool_boys:
                            bot.cool_boys.append(str(abn[1]))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)

            elif "/del_coolboys" in message.text and str(message.from_user.id) in ["832182441","741641254","987177223","5266773307"]:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if str(abn[1]) in bot.cool_boys:
                            bot.cool_boys.pop(bot.cool_boys.index(str(abn[1])))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)
            
            elif message.text=="/list_new_roles" and str(message.from_user.id) in bot.ids:
                prv=""

                if message.from_user.id in bot.people_can_change_role:
                    prv+="Совсем админы:\n"
                    for key in bot.people_can_change_role:
                        name=""
                        if str(key) in bot.auth:
                            name=f"{bot.auth[str(key)]} "
                        prv+=f"{name} {key}\n"

                
                if message.from_user.id in bot.people_admin or message.from_user.id in bot.people_can_change_role:
                    prv+="\nАдмины:\n"
                    for key in bot.people_admin:
                        name=""
                        if str(key) in bot.auth:
                            name=f"{bot.auth[str(key)]} "
                        prv+=f"{name} {key}\n"

                if message.from_user.id in bot.people_hueplekalo or message.from_user.id in bot.people_admin or message.from_user.id in bot.people_can_change_role:
                    prv+="\nТехники:\n"
                    for key in bot.people_hueplekalo:
                        name=""
                        if str(key) in bot.auth:
                            name=f"{bot.auth[str(key)]} "
                        prv+=f"{name} {key}\n"

                if prv=="": prv="Вы недостойны"
                
                bot.my_bot.send_message(message.from_user.id, prv)

            elif "/new_admin" in message.text and str(message.from_user.id) in bot.ids and message.from_user.id in bot.people_can_change_role:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if int(abn[1]) not in bot.people_admin:
                            bot.people_admin.append(int(abn[1]))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)

            elif "/new_rabotyaga" in message.text and str(message.from_user.id) in bot.ids and message.from_user.id in bot.people_can_change_role:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if int(abn[1]) not in bot.people_hueplekalo:
                            bot.people_hueplekalo.append(int(abn[1]))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)

            elif "/del_admin" in message.text and str(message.from_user.id) in bot.ids and message.from_user.id in bot.people_can_change_role:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if int(abn[1]) in bot.people_admin:
                            bot.people_admin.pop(bot.people_admin.index(int(abn[1])))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)

            elif "/del_rabotyaga" in message.text and str(message.from_user.id) in bot.ids and message.from_user.id in bot.people_can_change_role:
                abn=message.text.split()
                prv=""
                if len(abn)!=2:
                    prv="Вы не смогли"
                else:
                    try:
                        if int(abn[1]) in bot.people_hueplekalo:
                            bot.people_hueplekalo.pop(bot.people_hueplekalo.index(int(abn[1])))
                            bot.auth_save_data()
                        prv="Вы смогли"
                    except:
                        prv="Вы не смогли"
                
                bot.my_bot.send_message(message.from_user.id, prv)


    
            elif message.text=='/true_new_admin' and str(message.from_user.id) in bot.ids:
            	bot.au_new_admin(message)
            elif message.text=='/true_del_admin' and str(message.from_user.id) in bot.ids:
            	bot.au_del_admin(message)
            elif message.text=='/list_admin' and str(message.from_user.id) in bot.ids:
            	bot.au_list_admin(message)
             
            elif route=='au_new_admin': bot.au_new_admin2(message)
            elif route=='au_new_admin2': bot.au_new_admin3(message)
            elif route=='au_del_admin': bot.au_del_admin2(message)
            elif message.text=='/load_admin' and str(message.from_user.id) in bot.ids:
            	bot.au_load_admin(message)
            elif message.text=='/admin_help' and str(message.from_user.id) in bot.ids:
                bot.my_bot.send_message(message.from_user.id, '''
/new_admin - добавить нового администратора,
/list_admin - список администраторов,
/del_admin - удалить администратора,
/load_admin - перезагрузить список админов
    ''')
            
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#1':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#1']=htxt
                bot.users[str(message.from_user.id)]['route']='add_acc#2'
                bot.my_bot.send_message(message.from_user.id,'Пароль нового аккаунта сохранен. Введите список игр.', reply_markup=markupin)

            elif "почту" in message.text.lower() and "нахуй" in message.text.lower() or message.text=="/give_me_mail" or message.text=="Дай почту":
                db=shelve.open("/root/cndk-mail")
                mails=db.get("mails",[])
                db.close()
                
                while 1:
                    st=""
                    h1=["ho","ro","ma","ko","do","fu","to","mi","de","te","mu"]
                    h2=["u","o","a","y","i"]
                    h3=h1+h2
                    st+=random.choice(h1)
                    for i in range(3):
                        st+=random.choice(h3)
                    st+=str(random.randint(1000,9999))
                    st+="@cndkmail.com"
                    if st not in mails:
                        mails.append(st)
                        break
                if os.path.exists('/root/cndk-mail'): 
                    os.remove('/root/cndk-mail')
                db=shelve.open("/root/cndk-mail")
                db["mails"]=mails
                db.close()
                bot.my_bot.send_message(message.from_user.id,f"{st}")
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#2':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#2']=htxt
                bot.users[str(message.from_user.id)]['route']='add_acc#3'
                bot.my_bot.send_message(message.from_user.id,'Список игр сохранен. Отправьте фото QR-кода.', reply_markup=markupin)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#3':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                htxt=message.text
                if '/skip' in message.text:
                    htxt=''
                    bot.users[str(message.from_user.id)]['data_acc#3']=htxt
                    bot.users[str(message.from_user.id)]['route']='add_acc#4'
                    bot.my_bot.send_message(message.from_user.id,'QR код пропущен. Введите адрес почты.', reply_markup=markupin)
                else:
                    bot.my_bot.send_message(message.from_user.id,'Отправьте фото QR.', reply_markup=markupin)
                    
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#4':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#4']=htxt
                bot.users[str(message.from_user.id)]['route']='add_acc#451'
                bot.my_bot.send_message(message.from_user.id,'Почта сохранена. Отправьте дату рождения (не свою) в формате DD.MM.YYYY', reply_markup=markupin)
                    
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#451':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                #
                htxt=message.text
                pattern = r'^\d{2}\.\d{2}\.\d{4}$'
                if '/skip' in message.text: 
                    htxt=''
                    bot.users[str(message.from_user.id)]['data_acc#451']=htxt
                    bot.users[str(message.from_user.id)]['route']='add_acc#5'
                    bot.my_bot.send_message(message.from_user.id,'Дата рождения сохранена. Отправьте резервные коды.', reply_markup=markupin)
                elif re.match(pattern, htxt):
                    bot.users[str(message.from_user.id)]['data_acc#451']=htxt
                    bot.users[str(message.from_user.id)]['route']='add_acc#5'
                    bot.my_bot.send_message(message.from_user.id,'Дата рождения сохранена. Отправьте резервные коды.', reply_markup=markupin)
                else:
                    bot.my_bot.send_message(message.from_user.id,'Отправьте дату рождения (не свою) в формате DD.MM.YYYY или используйте /skip', reply_markup=markupin)
                
                    
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_acc#5':
                #
                if int(message.from_user.id) in bot.people_admin+bot.people_hueplekalo:
                    markupin=types.InlineKeyboardMarkup()
                    markupin.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='accept_'+str(message.from_user.id)))
                    markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                    #
                    htxt=message.text
                    if '/skip' in message.text: htxt=''
                    bot.users[str(message.from_user.id)]['data_acc#5']=htxt
                    bot.users[str(message.from_user.id)]['route']='add_acc#6'
                    gm=''
                    if bot.users[str(message.from_user.id)]['data_acc#2']!=[]:
                        gm=str(bot.users[str(message.from_user.id)]['data_acc#2'])
                    
                
                    
                        
                        
                    bot.my_bot.send_message(message.from_user.id,'Резервные коды сохранены. Подтвердите сохранение данных:\nАккаунт: '+bot.users[str(message.from_user.id)]['data_acc#0']+'\nПароль: '+bot.users[str(message.from_user.id)]['data_acc#1']+'\nИгры: '+gm+'\nПочта: '+bot.users[str(message.from_user.id)]['data_acc#4']+'\nРезервные коды:\n'+bot.users[str(message.from_user.id)]['data_acc#5'], reply_markup=markupin)
                else:
                    markupin=types.InlineKeyboardMarkup()
                    markupin.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='accept_'+str(message.from_user.id)))
                    markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+str(message.from_user.id)))
                    bot.users[str(message.from_user.id)]['data_acc#5']=""
                    bot.users[str(message.from_user.id)]['route']='add_acc#6'
                    
                    gm=''
                    if bot.users[str(message.from_user.id)]['data_acc#2']!=[]:
                        gm=str(bot.users[str(message.from_user.id)]['data_acc#2'])
                    bot.my_bot.send_message(message.from_user.id,'Резервные коды пропущены (вы недостойны их вводить). Подтвердите сохранение данных:\nАккаунт: '+bot.users[str(message.from_user.id)]['data_acc#0']+'\nПароль: '+bot.users[str(message.from_user.id)]['data_acc#1']+'\nИгры: '+gm+'\nПочта: '+bot.users[str(message.from_user.id)]['data_acc#4']+'\nРезервные коды:\n'+bot.users[str(message.from_user.id)]['data_acc#5'], reply_markup=markupin)
                
            

         
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='settings_acc' and message.text=="/add_game_acc":
                bot.users[str(message.from_user.id)]['route']='add_gm#0'
                bot.my_bot.send_message(message.from_user.id,'Введите название игры или выберите /back для отмены', reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_gm#0':
                bot.accs[bot.users[str(message.from_user.id)]['a']]['Игры']+=', '+message.text
                bot.save_data()
                bot.my_bot.send_message(message.from_user.id,'Игра добавлена на аккаунт. Введите следующую игру или выберите /back для отмены', reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='settings_acc' and message.text=="/list_game_acc":
                txt='Игр на аккаунте ('+str(len(bot.accs[bot.users[str(message.from_user.id)]['a']]['Игры']))+')\n'
                n=0
                for g in bot.accs[bot.users[str(message.from_user.id)]['a']]['Игры']:
                    txt+=g+' /delete_game_'+str(n)+' \n'
                    n+=1
                bot.my_bot.send_message(message.from_user.id,txt, reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='settings_acc' and message.text=="/press_acc":
                key=str(bot.get_day())
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                d=acc['Входы'].get(key,0)+1
                acc['Входы'][key]=d
                bot.little_save_data()
                a=0
                b=0
                for key2 in acc['Входы']:
                    if int(key)-int(key2)<=30:
                        a+=acc['Входы'][key2]
                    b+=acc['Входы'][key2]
                bot.my_bot.send_message(message.from_user.id,'Вход в аккаунт '+bot.users[str(message.from_user.id)]['a']+' #отмечен ('+str(a)+'/'+str(b)+')', reply_markup=markup)
                if acc.get('trade',False):
                        bot.my_bot.send_message(message.from_user.id,'Введите ID консоли и ник покупателя')
                        bot.users[str(message.from_user.id)]['route']='add_id'
                        bot.users[str(message.from_user.id)]['a']=login
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='settings_acc' and message.text=="/stat_acc":
                key=str(bot.get_day())
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                a=0
                b=0
                for key2 in acc['Входы']:
                    if int(key)-int(key2)<=30:
                        a+=acc['Входы'][key2]
                    b+=acc['Входы'][key2]
                bot.my_bot.send_message(message.from_user.id,'Входы за последние 30 дней: '+str(a)+'\nВходы за все время: '+str(b), reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='settings_acc' and message.text=="/clear_acc":
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                acc['Входы']={}
                bot.my_bot.send_message(message.from_user.id,'Входы очищены', reply_markup=markup)
            
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#0':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#0']=htxt
                bot.users[str(message.from_user.id)]['route']='change_acc#0_1'
                bot.my_bot.send_message(message.from_user.id,'Почта: '+acc['Почта']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#0_1':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#0_1']=htxt
                bot.users[str(message.from_user.id)]['route']='change_acc#1'
                bot.my_bot.send_message(message.from_user.id,'Игры: '+acc['Игры']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#1':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#1']=htxt
                if int(message.from_user.id) in bot.people_admin+bot.people_hueplekalo:
                    bot.users[str(message.from_user.id)]['route']='change_acc#1_1'
                    bot.my_bot.send_message(message.from_user.id,'Резервные коды: '+acc['Резервные коды']+'. Заполните поле', reply_markup=markupin)
                else:
                    
                    bot.users[str(message.from_user.id)]['data_acc#1_1']=""
                    bot.users[str(message.from_user.id)]['route']='change_acc#2'
                    bot.my_bot.send_message(message.from_user.id,'Дополнительно: '+acc['Дополнительно']+'. Заполните поле', reply_markup=markupin)
###!!!            

            elif message.text=="/aegis":
                tsv_data = bot.convert_shelve_to_tsv()
                
                if tsv_data:
                    bot.my_bot.send_message(for_reports, f"📊 Сгенерировано {len(tsv_data.split(chr(10)))} строк TSV")
                    bot.send_to_aegis(tsv_data)
                else:
                    bot.my_bot.send_message(for_reports, "❌ Нет данных для отправки")
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#1_1':
                #
                if int(message.from_user.id) in bot.people_admin+bot.people_hueplekalo:
                    markupin=types.InlineKeyboardMarkup()
                    markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                    markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                    #
                    acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                    htxt=message.text
                    if '/skip' in message.text: htxt=''
                    bot.users[str(message.from_user.id)]['data_acc#1_1']=htxt
                    bot.users[str(message.from_user.id)]['route']='change_acc#2'
                    bot.my_bot.send_message(message.from_user.id,'Дополнительно: '+acc['Дополнительно']+'. Заполните поле', reply_markup=markupin)
                else:
                    bot.users[str(message.from_user.id)]['data_acc#1_1']=""
                    bot.users[str(message.from_user.id)]['route']='change_acc#2'
                    bot.my_bot.send_message(message.from_user.id,'Дополнительно: '+acc['Дополнительно']+'. Заполните поле', reply_markup=markupin)

            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#2':
                #
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                htxt=message.text
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#2']=htxt
                bot.users[str(message.from_user.id)]['route']='change_acc#3'
                bot.my_bot.send_message(message.from_user.id,'Отправьте фото QR', reply_markup=markupin)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#3':
                #
                login=str(message.from_user.id)
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='reaccept_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(message.from_user.id)))
                #
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                htxt=''
                if '/skip' in message.text: htxt=''
                bot.users[str(message.from_user.id)]['data_acc#3']=htxt
                bot.users[str(message.from_user.id)]['route']='change_acc#4'
                login=str(message.from_user.id)
                
                bot.my_bot.send_message(message.from_user.id,'Пароль: '+acc['Пароль']+' -> '+bot.users[login]['data_acc#0']+'\nПочта: '+acc['Почта']+' -> '+
                                        bot.users[login]['data_acc#0_1']+'\nИгры: '+acc['Игры']+' -> '+bot.users[login]['data_acc#1']+'\nРезервные коды: '+acc['Резервные коды']+' -> '+bot.users[login]['data_acc#1_1']+'\nДополнительно: '+
                                        acc['Дополнительно']+' -> '+bot.users[login]['data_acc#2']+'\nПодтвердите изменение данных', reply_markup=markupin)

            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_acc#4':
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]

                caption=f"Изменение данных аккаунта {bot.users[str(message.from_user.id)]['a']}\n"
                if bot.users[str(message.from_user.id)]['data_acc#0']!='': caption+=f"{acc['Пароль']} -> {bot.users[str(message.from_user.id)]['data_acc#0']}\n"; acc['Пароль']=bot.users[str(message.from_user.id)]['data_acc#0']
                if bot.users[str(message.from_user.id)]['data_acc#0_1']!='': caption+=f"{acc['Почта']} -> {bot.users[str(message.from_user.id)]['data_acc#0_1']}\n"; acc['Почта']=bot.users[str(message.from_user.id)]['data_acc#0_1']
                if bot.users[str(message.from_user.id)]['data_acc#1']!='': caption+=f"{acc['Игры']} -> {bot.users[str(message.from_user.id)]['data_acc#1']}\n"; acc['Игры']=bot.users[str(message.from_user.id)]['data_acc#1']
                if bot.users[str(message.from_user.id)]['data_acc#1_1']!='': caption+=f"{acc['Резервные коды']} -> {bot.users[str(message.from_user.id)]['data_acc#1_1']}\n"; acc['Резервные коды']=bot.users[str(message.from_user.id)]['data_acc#1_1']
                if bot.users[str(message.from_user.id)]['data_acc#2']!='': caption+=f"{acc['Дополнительно']} -> {bot.users[str(message.from_user.id)]['data_acc#2']}\n"; acc['Дополнительно']=bot.users[str(message.from_user.id)]['data_acc#2']
                if bot.users[str(message.from_user.id)]['data_acc#3']!='': caption+=f"QR изменен\n"; acc['QR']=bot.users[str(message.from_user.id)]['data_acc#3']
                
                
                bot.users[str(message.from_user.id)]['route']=''
                bot.little_save_data()
                bot.my_bot.send_message(message.from_user.id,'Данные изменены', reply_markup=markup)
                bot.batya_report(caption,message.from_user.id)
                bot.clean_expired_change(message.from_user.id)
                bot.add_new_change(message.from_user.id)
                
                login=message.from_user.id
                try:
                    target_email = bot.users[str(login)]['data_acc#0_1'] if bot.users[str(login)]['data_acc#0_1'] else acc['Почта']
                    acc_info = bot.ams.get_account_id_by_email(target_email)
                    
                    if acc_info.get("ok"):
                        account_id = acc_info.get("accountId")
                        ams_update = {}
                        
                        if bot.users[str(login)]['data_acc#0']: ams_update["password"] = bot.users[str(login)]['data_acc#0']
                        if bot.users[str(login)]['data_acc#1']: ams_update["gameTitles"] = bot.users[str(login)]['data_acc#1'].split("\n")
                        if bot.users[str(login)]['data_acc#0_1']: ams_update["email"] = bot.users[str(login)]['data_acc#0_1']
                        if bot.users[str(login)]['data_acc#2']: ams_update["additionalInfo"] = [g.strip() for g in bot.users[str(login)]['data_acc#2'].split(',')]
                        if bot.users[str(login)]['data_acc#1_1']: ams_update["reserveCodes"] = [r.strip() for r in bot.users[str(login)]['data_acc#1_1'].split(',')]
                        
                        if ams_update:
                            upd_res = bot.ams.update_account(account_id, ams_update)
                            bot.my_bot.send_message(for_reports, f"🔄 отправка в AMS: {account_id}\n {ams_update}")
                            bot.my_bot.send_message(for_reports, f"🔄 ответ AMS: {upd_res}")
                            if upd_res.get("ok"):
                                bot.my_bot.send_message(for_reports, f"🔄 AMS: Аккаунт {target_email} обновлен")
                                bot.my_bot.send_message(login, f"🔄 AMS: Аккаунт {target_email} обновлен")
                            else:
                                bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка обновления: {upd_res}")
                                bot.my_bot.send_message(login, f"⚠️ AMS Ошибка обновления: {upd_res}")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления\n{acc_info}")
                        bot.my_bot.send_message(login, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления")
                except Exception as e:
                    bot.my_bot.send_message(for_reports, f"💥 AMS Exception (update): {traceback.format_exc()}")
                    bot.my_bot.send_message(login, f"💥 AMS Exception (update): {traceback.format_exc()}")

            

            elif message.text=="/check_maks_tek":
                bot.check_maks_tek()
                
                
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_usr#0':
                bot.users[str(message.from_user.id)]['data_usr#0']=message.text
                bot.users[str(message.from_user.id)]['route']='add_usr#1'
                bot.my_bot.send_message(message.from_user.id,'ID пользователя сохранено. Введите его имя или выберите /back для отмены', reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_usr#1':
                bot.users[str(message.from_user.id)]['route']=''
                bot.users[bot.users[str(message.from_user.id)]['data_usr#0']]={'name':message.text,'route':''}
                bot.little_save_data()
                bot.my_bot.send_message(message.from_user.id,'Пользователь добавлен', reply_markup=markup)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_id':
                bot.users[str(message.from_user.id)]['route']=''
                bot.accs[bot.users[str(message.from_user.id)]['a']]['id_client']=message.text
                bot.accs[bot.users[str(message.from_user.id)]['a']]['id_client_time']=time.time()
                bot.little_save_data()
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('7 дней',callback_data='days7_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('30 дней',callback_data='days30_'+str(message.from_user.id)))
                markupin.add(types.InlineKeyboardButton('Иное',callback_data='daysoth_'+str(message.from_user.id)))
                bot.my_bot.send_message(message.from_user.id,'ID консоли и ник покупателя добавлены. Выберите сроки аренды', reply_markup=markupin)
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='givemeyourpussypre':
                bot.users[str(message.from_user.id)]['a23']=message.text

                login=bot.users[str(message.from_user.id)]['a']
                
                markupin=types.InlineKeyboardMarkup()
                markupin.add(types.InlineKeyboardButton('Отправить код',callback_data='givemeyourpussy_'+login))
                markupin.add(types.InlineKeyboardButton('Отмена',callback_data='closeyourpussy_'+login))
                bot.users[str(message.from_user.id)]['route']='givemeyourpussy'
                bot.my_bot.send_message(message.from_user.id,'▶️ Выдача  '+login+'\n1️⃣ Введите код с консоли:',reply_markup=markupin)

            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='givemeyourpussy':
                bot.users[str(message.from_user.id)]['route']=''
                
                forwhy = bot.users[str(message.from_user.id)].get('a23')
                if not forwhy:
                    forwhy = "Unknown"
                code = message.text
                login = bot.users[str(message.from_user.id)]['a']
                password = bot.accs[bot.users[str(message.from_user.id)]['a']]['Пароль']
                mail = bot.accs[bot.users[str(message.from_user.id)]['a']]['Почта']
                bot.suchim(str(message.from_user.id), f"хочет выдать акк {login}")
                
                code_result = api.activate_nintendo(email=mail, code=code.upper())
                
                bot.users[str(message.from_user.id)]["a23"] = ""
                
                if code_result["status"] == "success":
                    task_id = code_result["task_id"]   
                    bot.maks_tek[task_id] = {
                        "user": str(message.from_user.id),
                        "status": "start",
                        "login": login,
                        "forwhy": forwhy,
                        "coding": code.upper()
                    }
                    bot.little_save_data()
                    bot.my_bot.send_message(message.from_user.id, f"⏳ Выдача {login}\n2️⃣ Операция в процессе")
                    bot.my_bot.send_message(message.from_user.id, "✅ Запрос принят. Ожидайте результат проверки...")
                    bot.my_bot.send_message(for_reports, "✅ Запрос принят. Ожидайте результат проверки...")
                
                elif code_result["status"] == "busy":
                    prv = (
                        f"⏸️ Аккаунт `{login}` сейчас занят другой операцией.\n"
                        f"Подождите 10–30 секунд и попробуйте снова.\n"
                        f"Если повторится — передайте задачу оператору."
                    )
                    bot.my_bot.send_message(message.from_user.id, escape_md_v2(prv), parse_mode="MarkdownV2")
                    bot.my_bot.send_message(for_reports, escape_md_v2(prv), parse_mode="MarkdownV2")
                
                else:
                    error_code = code_result.get("error_code", "") or ""
                    api_message = code_result.get("message", "Неизвестная ошибка")
                    
                    if error_code == "NintendoPasskeyNotFound":
                        prv = (
                            f"❗️ У аккаунта `{login}` отсутствует passkey.\n"
                            f"Автовыдача невозможна — передайте задачу технику или лиду направления."
                        )

                    elif error_code == "NintendoAccountDisabled":
                        prv = (
                            f"❌ Аккаунт `{login}` отключён или требует восстановления пароля.\n"
                            f"Необходима проверка техником в AMS."
                        )

                    elif error_code == "NintendoAccountNotFound":
                        prv = (
                            f"❌ Аккаунт `{login}` не найден в базе провайдера.\n"
                            f"Проверьте корректность e-mail или обратитесь к оператору."
                        )

                    elif "Code must be 8 symbols" in error_code:
                        prv = (
                            f"❌ Неверный формат кода консоли.\n"
                            f"Код должен содержать 8 символов (например: PLSD-YWXW).\n"
                            f"Получен: `{code.upper()}`"
                        )

                    elif "Email is required" in error_code:
                        prv = f"❌ У аккаунта `{login}` не заполнен e-mail. Передайте задачу технику."
  
                    elif error_code == "Timeout":
                        prv = (
                            f"⚠️ Сервер активации не ответил вовремя.\n"
                            f"Результат неизвестен — НЕ запускайте активацию повторно.\n"
                            f"Передайте задачу оператору для ручного поиска заявки."
                        )

                    elif error_code == "InternalError500":
                        prv = (
                            f"⚠️ Ошибка на стороне провайдера активации.\n"
                            f"Повторите попытку через 1–2 минуты.\n"
                            f"Если повторится — сообщите оператору."
                        )

                    else:
                        prv = f"❌ Ошибка при создании заявки: {api_message}"
                    
                    bot.my_bot.send_message(message.from_user.id, escape_md_v2(prv), parse_mode="MarkdownV2")
                    bot.my_bot.send_message(for_reports, escape_md_v2(prv), parse_mode="MarkdownV2")

            
            
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='add_id2':
                try:
                    tm=int(message.text)
                except:
                    bot.my_bot.send_message(message.from_user.id,'Пожалуйста, введите число', reply_markup=markup)
                    return 0
                bot.users[str(message.from_user.id)]['route']=''
                arr=['Срок аренды аккаунта '+bot.users[str(message.from_user.id)]['a']+' истекает. ID консоли и ник покупателя: '+bot.accs[bot.users[str(message.from_user.id)]['a']]['id_client'],
                 bot.accs[bot.users[str(message.from_user.id)]['a']]['id_client_time']+tm*24*60*60,2]
                bot.alarms4t[bot.users[str(message.from_user.id)]['a']]=arr
                bot.little_save_data()
                bot.my_bot.send_message(message.from_user.id,'Вы получите уведомление через '+str(tm-1)+' дней', reply_markup=markup)
            
                
            elif bot.users.get(str(message.from_user.id),{'route':''})['route']=='change_login':
                acc=bot.accs[bot.users[str(message.from_user.id)]['a']]
                bot.accs[message.text]=acc.copy()
                bot.accs.pop(bot.users[str(message.from_user.id)]['a'])
                
                
                bot.users[str(message.from_user.id)]['route']=''
                bot.little_save_data()
                bot.my_bot.send_message(message.from_user.id,'Данные изменены')
                bot.my_bot.send_message(for_reports,f'{bot.auth.get(str(message.from_user.id),str(message.from_user.id))} изменил логин аккаунта '+str(message.from_user.id)+' старый: '+bot.users[str(message.from_user.id)]['a']+' новый: '+message.text+'\n'+str(acc))
                
                
            else:

                found_accs = []

                for acc in bot.accs:
                    if str(message.text).strip() == str(bot.get_mname(acc)).strip() or message.text == f" {bot.get_mname(acc)}" or message.text == f"{bot.get_mname(acc)} ":
                        found_accs.append((1, acc))  

                for acc in bot.accs:
                    if re.fullmatch(r'\(' + re.escape(message.text) + r'\).*', acc):
                        found_accs.append((2, acc))

                for acc in bot.accs:
                    if re.fullmatch(r'\(.*\)' + re.escape(message.text), acc):
                        found_accs.append((3, acc))

                for acc in bot.accs:
                    if acc == 'cyndyk' + message.text:
                        found_accs.append((4, acc))
                    elif acc == 'sunacc' + message.text:
                        found_accs.append((4, acc))
                    elif acc == 'sunday' + message.text:
                        found_accs.append((4, acc))
                    elif acc == 'farezacc' + message.text:
                        found_accs.append((4, acc))
                    elif acc == 'pirat' + message.text:
                        found_accs.append((4, acc))
                    elif bot.accs[acc].get("Почта", "").lower() == message.text.lower():
                        found_accs.append((4, acc))

                sss = 0
                for i in range(10):
                    sss += message.text.count(str(i))

                if sss < len(message.text):
                    for acc in bot.accs:
                        if message.text in acc:
                            found_accs.append((5, acc))


                if bot.accs.get(message.text.lower(), {}):
                    found_accs.append((1, message.text.lower()))

                unique_accs = {}
                for priority, acc_key in found_accs:
                    if acc_key not in unique_accs or priority < unique_accs[acc_key]:
                        unique_accs[acc_key] = priority

                sorted_accs = sorted(unique_accs.items(), key=lambda x: x[1])


                top_accs = sorted_accs[:3]


                if top_accs:
                    for fnm, priority  in top_accs:

                        acc = bot.accs[fnm]
                        bot.get_info(message, fnm, False)
                else:

                    try:
                        db = shelve.open(DEL_ACCS_DATA_SHELVE)
                        del_accs = db.get("del_accs", {})
                        db.close()
                        
                        if os.path.exists(DEL_ACCS_DATA_SHELVE): 
                            os.remove(DEL_ACCS_DATA_SHELVE)
                        
                        db = shelve.open(DEL_ACCS_DATA_SHELVE)
                        db["del_accs"]=del_accs 
                        db.close()
                    except Exception:
                        del_accs = {}
                    
                    chj = True
                    for acci in del_accs:
                        if message.text.lower() in acci.lower():
                            chj = False
                            bot.my_bot.send_message(message.from_user.id, del_accs[acci]["Удален"])
                            break
                    
                    if chj:
                        bot.my_bot.send_message(message.from_user.id, 'Аккаунт не найден', reply_markup=markup)
        
        else:
            bot.my_bot.send_message(message.from_user.id, 'Ты мне не нравишься')
            bot.my_bot.send_message(for_reports, f'Ты мне не нравишься {str(message.from_user.id)} {str(message.from_user.id) in bot.ids}')

        	
    except Exception as e:
        bot.my_bot.send_message(for_reports,message.text)
        bot.my_bot.send_message(for_reports,traceback.format_exc())
        
        bot.imt(message.from_user.id,str(traceback.format_exc()))
        debag(traceback.format_exc())
        
@bot.my_bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    try:

        ind=callback.data.find('_')
        comm=callback.data[:ind]
        login=callback.data[ind+1:]
        
        current_time = time.time()
        if str(callback.from_user.id) in bad_boys and str(callback.from_user.id) not in bot.cool_boys or str(callback.from_user.id) not in bot.ids:
            bot.my_bot.send_message(callback.from_user.id,'Я тебя целенаправленно игнорю')

        elif bot.is_night_time() and str(callback.from_user.id) not in bot.cool_boys:
            bot.my_bot.send_message(callback.from_user.id,'Я сплю, потому что ты недостаточно хорош, чтобы я тебе отвечал')
        elif comm=='vhod':
            vhods=bot.mega_kost.get(callback.from_user.id,['',0])
            if vhods[0]==login and time.time()-vhods[1]<80:
                bot.my_bot.send_message(callback.from_user.id,'Вход в аккаунт '+login+' не отмечен (предыдущая отметка была менее минуты назад)')
            else:
                bot.mega_kost[callback.from_user.id]=[login,time.time()]
                
                ams_acc = bot.ams_get_acc_by_login(login)
                if ams_acc:
                    account_id = ams_acc.get("accountId")
                    new_logins_total = ams_acc.get("loginsTotal", 0) + 1
                    new_logins_30d = ams_acc.get("logins30d", 0) + 1
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    patch_data = {
                        "loginsTotal": new_logins_total,
                        "logins30d": new_logins_30d,
                        "lastLogins": now_str,
                        "reason": f"Manual login mark by manager {callback.from_user.id}"
                    }
                    patch_res = bot.ams.update_account(account_id, patch_data)
                    
                    if patch_res.get("ok"):
                        bot.my_bot.send_message(callback.from_user.id, f'Вход в аккаунт {login} #отмечен ({new_logins_30d}/{new_logins_total})')
                    else:
                        try:
                            bot.my_bot.send_message(callback.from_user.id, f'⚠️ Вход отмечен локально, но AMS не ответил: {patch_res.get("error", "unknown")}')
                            bot.my_bot.send_message(callback.from_user.id, f'⚠️ Вход отмечен локально, но AMS не ответил: {patch_res}')
                            bot.my_bot.send_message(for_reports, f'⚠️ Вход отмечен локально, но AMS не ответил: {patch_res}')
                        except:
                            pass
                        acc = bot.accs.get(login, {'Входы': {}})
                        key = str(bot.get_day())
                        acc['Входы'][key] = acc['Входы'].get(key, 0) + 1
                        bot.accs[login] = acc
                        bot.little_save_data()
                else:
                    acc = bot.accs.get(login, {'Входы': {}})
                    key = str(bot.get_day())
                    acc['Входы'][key] = acc['Входы'].get(key, 0) + 1
                    bot.accs[login] = acc
                    bot.little_save_data()
                    bot.my_bot.send_message(callback.from_user.id, f'Вход в аккаунт {login} #отмечен (локально, AMS не найден)')
                acc = bot.accs.get(login, {})
                if acc.get('trade', False):
                    bot.my_bot.send_message(callback.from_user.id, 'Введите ID консоли и ник покупателя')
                    bot.users[str(callback.from_user.id)]['route'] = 'add_id'
                    bot.users[str(callback.from_user.id)]['a'] = login
        elif comm=="folderchange":
            fnm=login
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Изменить 2FA через QR',callback_data="change2FAwithQR_"+fnm))
            markupin.add(types.InlineKeyboardButton('Изменить данные аккаунта',callback_data='changeacc_'+fnm))
            markupin.add(types.InlineKeyboardButton('Изменить номер и логин аккаунта',callback_data='changelogin_'+fnm))
            markupin.add(types.InlineKeyboardButton('Основа продана',callback_data='sellbase_'+fnm))
            markupin.add(types.InlineKeyboardButton('Основа  не продана',callback_data='notsellbase_'+fnm))
            markupin.add(types.InlineKeyboardButton('Вернуться',callback_data='delthismessage_'+fnm))
            bot.my_bot.send_message(callback.from_user.id,"Изменить данные", reply_markup=markupin)
        elif comm=="delthismessage":
            bot.my_bot.delete_message(callback.message.chat.id, callback.message.message_id)
        elif comm=='2fa':
            bot.suchim(str(callback.from_user.id),f"хочет 2fa для {login}")

            colling=0
            try:
                email = bot.accs[login]['Почта']
                ams_info = bot.ams.get_account_id_by_email(email)
                if ams_info.get("ok"):
                    ams_account_id = ams_info.get("accountId", "")

                    ams_info2 = bot.ams.get_2fa_code(ams_account_id)

                    if ams_info2.get("code"):
                        colling=1
                        code=ams_info2["code"]
                        bot.my_bot.send_message(callback.from_user.id,'Текущий код. \nКод выдан для '+ams_info2["email"])
                        bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(code))+'```', parse_mode='MarkdownV2')
                        if ams_info2["expiresInSeconds"]<25:
                            bot.my_bot.send_message(callback.from_user.id,'Код будет выслан еще раз через '+str(ams_info2["expiresInSeconds"])+' сек.')
                            time.sleep(ams_info2["expiresInSeconds"]+1.5)

                            ams_info2 = bot.ams.get_2fa_code(ams_account_id)

                            if ams_info2.get("code"):
                                colling=1
                                code=ams_info2["code"]
                                bot.my_bot.send_message(callback.from_user.id,'Текущий код. \nКод выдан для '+ams_info2["email"])
                                bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(code))+'```', parse_mode='MarkdownV2')
                    elif ams_info2["ok"]==False and "has no usable totp secret" in ams_info2["detail"]:
                        bot.my_bot.send_message(callback.from_user.id,'В амс кода нет')
            except:
                bot.my_bot.send_message(callback.from_user.id,'АМС не сработало')


            if colling==0:

                st1=login
                st2=''

                if (re.fullmatch(r'.*(.*).*',login) or re.fullmatch(r'(.*).*',login)) and login.find(')')!=-1:
                    ind=login.index(')')
                    if '(' in login:
                        ind2=login.index('(')+1
                    else:
                        ind2=0
                    st1=login[ind+1:]
                    st2=login[ind2:ind]
                else:
                    for su in login:
                        if su in '1234567890':
                            st2+=su
                ss=int(time.time())%30
                ss=30-ss
                lg1,ss1,byaka1=bot.give_your_password(st1)
                lg2,ss2,byaka2=bot.give_your_password(st2)
                byaka=False
                if byaka1 or byaka2:
                    byaka=True
                if lg1=='Не найдено':
                    lg1,lg2=lg2,lg1
                    ss1,ss2=ss2,ss1
                if lg1!='Не найдено':
                    bot.my_bot.send_message(callback.from_user.id,'Текущий код. \nКод выдан для '+lg1)
                    bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(ss1))+'```', parse_mode='MarkdownV2')
                    if ss1!=ss2 and lg2!='Не найдено' and byaka==False:
                        bot.my_bot.send_message(callback.from_user.id,'Текущий код\nКод выдан для '+lg2)
                        bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(ss2))+'```', parse_mode='MarkdownV2')
                else:
                    bot.my_bot.send_message(callback.from_user.id,'Код в базе не обнаружен')
                #
                if ss<25 and (lg1!="Не найдено" or lg2!="Не найдено"):
                    bot.my_bot.send_message(callback.from_user.id,'Код будет выслан еще раз через '+str(ss)+' сек.')
                    time.sleep(ss+1.5)
                    lg1,ss1,byaka1=bot.give_your_password(st1)
                    lg2,ss2,byaka2=bot.give_your_password(st2)

                    byaka=False
                    if byaka1 or byaka2:
                        byaka=True

                    if lg1=='Не найдено':
                        lg1,lg2=lg2,lg1
                        ss1,ss2=ss2,ss1
                    if lg1!='Не найдено':
                        bot.my_bot.send_message(callback.from_user.id,'Текущий код. \nКод выдан для '+lg1)
                        bot.my_bot.send_message(callback.from_user.id,str(ss1))
                        bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(ss1))+'```', parse_mode='MarkdownV2')
                        if ss1!=ss2 and lg2!='Не найдено' and byaka==False:
                            bot.my_bot.send_message(callback.from_user.id,'Текущий код\nКод выдан для '+lg2)
                            bot.my_bot.send_message(callback.from_user.id,str(ss2))
                            bot.my_bot.send_message(callback.from_user.id,'```2FA:\n'+bot.escape_markdown_v2(str(ss2))+'```', parse_mode='MarkdownV2')
                    else:
                        bot.my_bot.send_message(callback.from_user.id,'Код в базе не обнаружен')
        elif comm == "givemeyourpussy":
            user_id = str(callback.from_user.id)
                
            bot.users[user_id]['a'] = login
            existing_a23 = bot.users.get(user_id, {}).get('a23')

            if existing_a23:
                markupin = types.InlineKeyboardMarkup(row_width=2) 
                markupin.add(
                        types.InlineKeyboardButton('📤 Отправить код', callback_data=f'givemeyourpussy2_{login}'),
                        types.InlineKeyboardButton('🔄 Сбросить имя', callback_data=f'resetclient_{login}')
                    )
                    
                bot.users[user_id]['route'] = 'givemeyourpussy'
                bot.my_bot.send_message(
                        callback.from_user.id,
                        f'▶️ Выдача {login}\n👤 Клиент: <b>{existing_a23}</b>\n\n1️⃣ Введите код с консоли:',
                        reply_markup=markupin,
                        parse_mode="HTML"
                    )
            else:
                bot.users[user_id]['route'] = 'givemeyourpussypre'
                bot.my_bot.send_message(
                        callback.from_user.id,
                        f'▶️ Выдача {login}\n(0) Введите имя клиента или ссылку на него:'
                    )
                
            bot.my_bot.answer_callback_query(callback.id)

        elif comm == "closeyourpussy":
            user_id = str(callback.from_user.id)
            bot.users[user_id]['route']=''
            bot.users[user_id]["a23"]=""
            bot.my_bot.send_message(
                        callback.from_user.id,
                        f'Отмена (сам текст придумывать не буду, поэтому скучная ОТМЕНА)'
                    )


            

        elif comm == "resetclient":
            user_id = str(callback.from_user.id)
            if 'a23' in bot.users.get(user_id, {}):
                del bot.users[user_id]['a23']
                
            bot.users[user_id]['route'] = 'givemeyourpussypre'
            bot.users[user_id]['a'] = login 
                
            bot.my_bot.send_message(
                    callback.from_user.id,
                    f'✏️ Имя клиента сброшено.\n\nВведите новое имя клиента или ссылку на него для выдачи {login}:'
                )
                
            bot.my_bot.answer_callback_query(callback.id, "Имя клиента сброшено")
        elif comm == 'delvhod':
            ams_acc = bot.ams_get_acc_by_login(login)
            api_ok = False
            
            if ams_acc:
                account_id = ams_acc.get("accountId")
                usages_res = bot.ams.get_account_usages(account_id, include_released=False)
                
                if usages_res.get("ok"):
                    items = usages_res.get("items", [])
                    active = [u for u in items if u.get("active")]
                    
                    if active:
                        active.sort(key=lambda x: x.get("assignedAtUtc", ""), reverse=True)
                        last_usage = active[0]
                        usage_id = last_usage.get("usageId")
                        
                        reason = f"Cancel last login by manager {callback.from_user.id}"
                        rel_res = bot.ams.release_usage(account_id, usage_id, reason=reason)
                        
                        if rel_res.get("ok"):
                            api_ok = True
                            bot.my_bot.send_message(
                                callback.from_user.id,
                                f'✅ Последний вход на аккаунт {login} отменён через AMS'
                            )
                        else:
                            bot.my_bot.send_message(
                                callback.from_user.id,
                                f'⚠️ Ошибка отмены в AMS: {rel_res.get("error", "unknown")}'
                            )
                    else:
                        bot.my_bot.send_message(callback.from_user.id, 'Нет активных входов для отмены')
                        api_ok = True  
                else:
                    bot.my_bot.send_message(
                        callback.from_user.id,
                        f'⚠️ Не удалось получить список входов: {usages_res.get("error", "unknown")}'
                    )
            
            if not api_ok:
                acc = bot.accs[login]
                st = ''
                key = ''
                for key in acc['Входы']:
                    st = key
                if st != '' and key != '':
                    acc['Входы'][key] -= 1
                    if acc['Входы'][key] <= 0:
                        acc['Входы'].pop(key)
                    bot.little_save_data()
                    bot.my_bot.send_message(callback.from_user.id, f'Вход в аккаунт {login} отменён (локально)')
                else:
                    bot.my_bot.send_message(callback.from_user.id, f'Нет входов для отмены на аккаунте {login}')
                
                    
                
    
        elif comm=='revhod45':
            ind=login.find(' _^_ ')
            login2=login[:ind]
            key=login[ind+5:]
            
            acc=bot.accs[login2]
            d=acc['Входы'].get(key,0)-1
            if d>=0:
                acc['Входы'][key]=d
                db=shelve.open(BOT_END_DATA_SHELVE)
                table_vhods=db.get('table_vhods',{})
                d2=table_vhods.get(login,0)
                if d2>0:
                    d2-=1
                    table_vhods[login]=d2
                    db['table_vhods']=table_vhods
                db.close()
                bot.my_bot.send_message(callback.from_user.id,'Вход отменен')
                
        elif comm=='del':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Удалить',callback_data='trydel_'+login))
            bot.my_bot.send_message(callback.from_user.id,'Вы действительно хотите удалить этот аккаунт?',reply_markup=markupin)
            
        elif comm=='trydel':
            current_date = datetime.now()
            fd = current_date.strftime("%d.%m.%Y")
            username=bot.auth.get(str(callback.from_user.id),str(callback.from_user.id))
            rep=f"❌ Аккаунт {login} удален {fd} менеджером {username}"
            bot.my_bot.send_message(for_reports,rep)
            bot.my_bot.send_message('832182441',rep)

            email = bot.accs[login].get('Почта', '')

            db=shelve.open(DEL_ACCS_DATA_SHELVE)
            del_accs=db.get("del_accs",{})
            dacc=bot.accs[login]
            dacc["Удален"]=rep
            del_accs[login]=dacc
            db["del_accs"]=del_accs
            db.close()
            
            
            bot.accs.pop(login)
            bot.save_data()
            login2 = callback.from_user.id

            
            acc_info = bot.ams.get_account_id_by_email(email)
                    
            if acc_info.get("ok"):
                account_id = acc_info.get("accountId")
                ams_update = {"userTag": str(username),"lifecycleStatus":"deleted"}

                if ams_update:
                    upd_res = bot.ams.update_account(account_id, ams_update)
                    bot.my_bot.send_message(for_reports, f"🔄 отправка в AMS: {account_id}\n {ams_update}")
                    bot.my_bot.send_message(for_reports, f"🔄 ответ AMS: {upd_res}")
                    if upd_res.get("ok"):
                        bot.my_bot.send_message(for_reports, f"🔄 AMS: Аккаунт {email} удален")
                        bot.my_bot.send_message(login2, f"🔄 AMS: Аккаунт {email} удален")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка удаления: {upd_res}")
                        bot.my_bot.send_message(login2, f"⚠️ AMS Ошибка удаления: {upd_res}")
            else:
                bot.my_bot.send_message(for_reports, f"⚠️ AMS: Аккаунт с почтой {email} не найден в мастер-базе для удаления\n{acc_info}")
                bot.my_bot.send_message(login2, f"⚠️ AMS: Аккаунт с почтой {email} не найден в мастер-базе для удаления")
            
            bot.clean_expired_change(callback.from_user.id)
            bot.add_new_change(callback.from_user.id)
        elif comm=='gback':
            bot.users[str(login)]['route']=''
            bot.my_bot.send_message(callback.from_user.id,'Добавление аккаунта отменено')
        elif comm=='regback':
            bot.users[str(login)]['route']=''
            bot.my_bot.send_message(callback.from_user.id,'Изменение аккаунта отменено')
        elif comm=='skip':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='skip_'+login))
            markupin.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+login))
            
            markupin2=types.InlineKeyboardMarkup()
            markupin2.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='accept_'+login))
            markupin2.add(types.InlineKeyboardButton('Отменить добавление',callback_data='gback_'+login))
            if bot.users.get(str(login),{'route':''})['route']=='add_acc#1':
                bot.users[login]['data_acc#1']=''
                bot.users[login]['route']='add_acc#2'
                bot.my_bot.send_message(login,'Введите список игр через запятую', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='add_acc#2':
                bot.users[login]['data_acc#2']=''
                bot.users[login]['route']='add_acc#3'
                bot.my_bot.send_message(login,'Отправьте фото QR-кода', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='add_acc#3':
                bot.users[login]['data_acc#3']=''
                bot.users[login]['route']='add_acc#4'
                bot.my_bot.send_message(login,'Введите адрес электронной почты', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='add_acc#4':
                bot.users[login]['data_acc#4']=''
                bot.users[login]['route']='add_acc#451'
                bot.my_bot.send_message(login,'Введите дату рождения (не свою) в формате DD.MM.YYYY', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='add_acc#451':
                bot.users[login]['data_acc#4']=''
                if int(login) in bot.people_admin+bot.people_hueplekalo:
                    bot.users[login]['route']='add_acc#5'
                    bot.my_bot.send_message(login,'Введите резервные коды', reply_markup=markupin)
                else:
                    bot.users[login]['data_acc#5']=''
                    bot.users[login]['route']='add_acc#6'
                    bot.my_bot.send_message(login,'Подтвердите сохранение данных:\nАккаунт: '+bot.users[login]['data_acc#0']+'\nПароль: '+bot.users[login]['data_acc#1']+'\nИгры: '+str(bot.users[login]['data_acc#2'])+'\nПочта: '+bot.users[login]['data_acc#4']+'\nРезервные коды:\n'+bot.users[login]['data_acc#5'], reply_markup=markupin2)
            elif bot.users.get(str(login),{'route':''})['route']=='add_acc#5':
                bot.users[login]['data_acc#5']=''
                bot.users[login]['route']='add_acc#6'
                bot.my_bot.send_message(login,'Подтвердите сохранение данных:\nАккаунт: '+bot.users[login]['data_acc#0']+'\nПароль: '+bot.users[login]['data_acc#1']+'\nИгры: '+str(bot.users[login]['data_acc#2'])+'\nПочта: '+bot.users[login]['data_acc#4']+'\nРезервные коды:\n'+bot.users[login]['data_acc#5'], reply_markup=markupin2)
        elif comm=="erroracc":
            bot.errors_acc[login]=time.time()
            bot.my_bot.send_message(callback.from_user.id,'Аккаунт отключен на 2 часа')
        elif comm=='reskip':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+login))
            markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+login))
            
            markupin2=types.InlineKeyboardMarkup()
            markupin2.add(types.InlineKeyboardButton('Подтвердить данные',callback_data='reaccept_'+login))
            markupin2.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+login))
            acc=bot.accs[bot.users[login]['a']]
            
            
            if bot.users.get(str(login),{'route':''})['route']=='change_acc#0':
                bot.users[login]['data_acc#0']=''
                bot.users[login]['route']='change_acc#0_1'
                bot.my_bot.send_message(callback.from_user.id,'Почта: '+acc['Почта']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='change_acc#0_1':
                bot.users[login]['data_acc#0_1']=''
                bot.users[login]['route']='change_acc#1'
                bot.my_bot.send_message(callback.from_user.id,'Игры: '+acc['Игры']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='change_acc#1':
                bot.users[login]['data_acc#1']=''
                if int(login) in bot.people_admin+bot.people_hueplekalo:
                    bot.users[login]['route']='change_acc#1_1'
                    bot.my_bot.send_message(callback.from_user.id,'Резервные коды: '+acc['Резервные коды']+'. Заполните поле', reply_markup=markupin)
                else:
                    
                    bot.users[login]['data_acc#1_1']=''
                    bot.users[login]['route']='change_acc#2'
                    bot.my_bot.send_message(callback.from_user.id,'Дополнительно: '+acc['Дополнительно']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='change_acc#1_1':
                bot.users[login]['data_acc#1_1']=''
                bot.users[login]['route']='change_acc#2'
                bot.my_bot.send_message(callback.from_user.id,'Дополнительно: '+acc['Дополнительно']+'. Заполните поле', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='change_acc#2':
                bot.users[login]['data_acc#2']=''
                bot.users[login]['route']='change_acc#3'
                bot.my_bot.send_message(callback.from_user.id,'Отправьте новое фото QR', reply_markup=markupin)
            elif bot.users.get(str(login),{'route':''})['route']=='change_acc#3':
                bot.users[login]['data_acc#3']=''
                bot.users[login]['route']='change_acc#4'
                
                bot.my_bot.send_message(callback.from_user.id,'Пароль: '+acc['Пароль']+' -> '+bot.users[login]['data_acc#0']+'\nПочта: '+acc['Почта']+' -> '+
                                        bot.users[login]['data_acc#0_1']+'\nИгры: '+acc['Игры']+' -> '+bot.users[login]['data_acc#1']+'\nРезервные коды: '+acc['Резервные коды']+' -> '+bot.users[login]['data_acc#1_1']+'\nДополнительно: '+
                                        acc['Дополнительно']+' -> '+bot.users[login]['data_acc#2']+'\nПодтвердите изменение данных', reply_markup=markupin2)
            

        elif comm=='info':
            try:
                ind=login.rfind('_')
                login2=login[ind+1:]
                login=login[:ind]
                acc=bot.accs[login]
                bot.get_info(callback,login,True)
            except Exception as e:
                bot.my_bot.send_message(for_reports,traceback.format_exc())
                bot.imt(callback.from_user.id,str(traceback.format_exc()))
                debag(traceback.format_exc())

#
        
        elif comm=='pagisosi':
            if bot.pagination[str(login)] is not None:
               bot.draw_page(bot.pagination[str(login)],bot.page[str(login)],20,int(login))
        elif comm=='pagisosimnogo':
            if bot.pagination[str(login)] is not None:
               bot.draw_page(bot.pagination[str(login)],bot.page[str(login)],23,int(login))
        elif comm=='pagidie':
            bot.pagination[str(login)]=None
#
        elif comm=='ENinfo':
            try:
                ind=login.rfind('_')
                login2=login[ind+1:]
                login=login[:ind]
                acc=bot.accs[login]
                bot.get_info(callback,login,True)
            except Exception as e:
                bot.my_bot.send_message(for_reports,traceback.format_exc())
                
                bot.imt(callback.from_user.id,str(traceback.format_exc()))
                debag(traceback.format_exc())
        elif comm=='clearvh':
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Очистить входы',callback_data='clearvhaccept_'+login))
            bot.my_bot.send_message(callback.from_user.id,'Вы уверены, что хотите очистить входы?',reply_markup=markupin)
        elif comm == 'clearvhaccept':
            ams_acc = bot.ams_get_acc_by_login(login)
            api_ok = False
            
            if ams_acc:
                account_id = ams_acc.get("accountId")
                reason = f"Clear logins by manager {callback.from_user.id}"
                
                patch_res = bot.ams.release_all_usages(account_id, reason=reason)
                
                if patch_res.get("ok"):
                    api_ok = True
                    bot.my_bot.send_message(
                        callback.from_user.id,
                        f'✅ Все входы для аккаунта {login} очищены в AMS'
                    )
                else:
                    bot.my_bot.send_message(
                        callback.from_user.id,
                        f'⚠️ Ошибка очистки входов в AMS: {patch_res.get("error", "unknown")}'
                    )
            if not api_ok:
                bot.accs[login]['Входы'] = {}
                bot.save_data()
                bot.my_bot.send_message(
                    callback.from_user.id,
                    f'Входы для аккаунта {login} очищены (локально)'
                )
            ohm = bot.auth.get(str(callback.from_user.id), "")
            if ohm == "":
                ohm = bot.users.get(str(callback.from_user.id), {}).get("name", "")
            if ohm == "":
                ohm = str(callback.from_user.id)
            
            today = datetime.now().strftime("%d.%m.%Y")
            bot.accs[login]["Очиститель"] = ohm
            bot.accs[login]["Очищено"] = today
            bot.little_save_data()
            
            for id in bot.ids:
                msg = f"🧹 Входы на аккаунт {login} очищены менеджером: {ohm}"
                bot.my_bot.send_message(id, msg)
        elif comm=='changelogin':
            bot.users[str(callback.from_user.id)]['a']=login
            acc=bot.accs[bot.users[str(callback.from_user.id)]['a']]
            bot.users[str(callback.from_user.id)]['route']='change_login'
            bot.my_bot.send_message(callback.from_user.id,'Текущий логин: '+login+'. Введите новый или примените команду /back (/break) для отмены')
        elif comm=='changeacc':
            #
            markupin=types.InlineKeyboardMarkup()
            markupin.add(types.InlineKeyboardButton('Пропустить пункт',callback_data='reskip_'+str(callback.from_user.id)))
            markupin.add(types.InlineKeyboardButton('Отменить редактирование',callback_data='regback_'+str(callback.from_user.id)))
                #
            bot.users[str(callback.from_user.id)]['a']=login
            acc=bot.accs[bot.users[str(callback.from_user.id)]['a']]
            bot.users[str(callback.from_user.id)]['route']='change_acc#0'
            bot.my_bot.send_message(callback.from_user.id,'Текущий пароль: '+acc['Пароль']+'. Введите новый',reply_markup=markupin)
            
        elif comm=='changetrade':
            trade=bot.accs[login].get('trade',False)
            if trade:
                trade=False
            else:
                trade=True
            bot.accs[login]['trade']=trade
            bot.save_data()
            if trade:
                bot.my_bot.send_message(callback.from_user.id,'Теперь этот аккаунт сдается в аренду')
            else:
                bot.my_bot.send_message(callback.from_user.id,'Этот аккаунт больше не в аренде')
                bot.alarms4t[login]=[]
        elif comm=="sellbase":
            acc=bot.accs[login]
            dp=acc["Дополнительно"]
            dp2=acc["Дополнительно"]
            if "основа не продана" in dp:
                dp=dp.replace("основа не продана", "").strip()
            if "⚠️" in dp:
                dp=dp.replace("⚠️", "").strip()
            if "основа" in dp:
                dp=dp.replace("основа", "").strip()
            bot.accs[login]["Дополнительно"]=dp

            
            login2=callback.from_user.id
            try:
                target_email = acc['Почта']
                acc_info = bot.ams.get_account_id_by_email(target_email)
                    
                if acc_info.get("ok"):
                    account_id = acc_info.get("accountId")
                    ams_update = {}
                    ams_update["additionalInfo"] = dp

                    upd_res = bot.ams.update_account(account_id, ams_update)
                    bot.my_bot.send_message(for_reports, f"🔄 отправка в AMS: {account_id}\n {ams_update}")
                    bot.my_bot.send_message(for_reports, f"🔄 ответ AMS: {upd_res}")
                    if upd_res.get("ok"):
                        bot.my_bot.send_message(for_reports, f"🔄 AMS: Аккаунт {target_email} обновлен")
                        bot.my_bot.send_message(login2, f"🔄 AMS: Аккаунт {target_email} обновлен")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка обновления: {upd_res}")
                        bot.my_bot.send_message(login2, f"⚠️ AMS Ошибка обновления: {upd_res}")
                else:
                    bot.my_bot.send_message(for_reports, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления\n{acc_info}")
                    bot.my_bot.send_message(login2, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления")
            except Exception as e:
                bot.my_bot.send_message(for_reports, f"💥 AMS Exception (update): {traceback.format_exc()}")
                bot.my_bot.send_message(login2, f"💥 AMS Exception (update): {traceback.format_exc()}")
            
        elif comm=="notsellbase":
            acc=bot.accs[login]
            dp=acc["Дополнительно"]
            dp2=acc["Дополнительно"]
            dp+=" основа не продана"
            bot.accs[login]["Дополнительно"]=dp

            login2=callback.from_user.id
            try:
                target_email = acc['Почта']
                acc_info = bot.ams.get_account_id_by_email(target_email)
                    
                if acc_info.get("ok"):
                    account_id = acc_info.get("accountId")
                    ams_update = {}
                    ams_update["additionalInfo"] = dp

                    upd_res = bot.ams.update_account(account_id, ams_update)
                    bot.my_bot.send_message(for_reports, f"🔄 отправка в AMS: {account_id}\n {ams_update}")
                    bot.my_bot.send_message(for_reports, f"🔄 ответ AMS: {upd_res}")
                    if upd_res.get("ok"):
                        bot.my_bot.send_message(for_reports, f"🔄 AMS: Аккаунт {target_email} обновлен")
                        bot.my_bot.send_message(login2, f"🔄 AMS: Аккаунт {target_email} обновлен")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка обновления: {upd_res}")
                        bot.my_bot.send_message(login2, f"⚠️ AMS Ошибка обновления: {upd_res}")
                else:
                    bot.my_bot.send_message(for_reports, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления\n{acc_info}")
                    bot.my_bot.send_message(login2, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления")
            except Exception as e:
                bot.my_bot.send_message(for_reports, f"💥 AMS Exception (update): {traceback.format_exc()}")
                bot.my_bot.send_message(login2, f"💥 AMS Exception (update): {traceback.format_exc()}")
            
            
        elif comm=="change2FAwithQR":
            bot.users[str(callback.from_user.id)]['route']='send_qr_2fa'
            bot.users[str(callback.from_user.id)]['set_acc']=login
            bot.my_bot.send_message(callback.from_user.id,'Отправьте фото QR или используйте команду /back (/break), если передумали отправлять QR')
            
        elif comm=='accept':
            
            if bot.users.get(str(login),{'route':''})['route']=='add_acc#6':
                bot.accs[bot.users[str(login)]['data_acc#0']]={
                        'Пароль':bot.users[str(login)]['data_acc#1'],
                        'Почта':bot.users[str(login)]['data_acc#4'],
                        'Игры':bot.users[str(login)]['data_acc#2'],
                        'QR': bot.users[str(login)]['data_acc#3'],
                        'Входы':{},
                        'Дата рождения': bot.users[str(login)]['data_acc#451'],
                        'Дополнительно': '',
                        'Резервные коды':bot.users[str(login)]['data_acc#5']
                    }
                
                bot.users[str(login)]['route']=''
                bot.save_data()

                try:
                    ams_payload = {
                        "accountCode": bot.users[str(login)]['data_acc#0'],
                        "loginId": bot.users[str(login)]['data_acc#0'],
                        "password": bot.users[str(login)]['data_acc#1'],
                        "email": bot.users[str(login)]['data_acc#4'],
                        "birthDate": bot.users[str(login)]['data_acc#451'],
                        "gameTitles": [g.strip() for g in str(bot.users[str(login)]['data_acc#2']).split(',') if g.strip()],
                        "reserveCodes": [r.strip() for r in str(bot.users[str(login)]['data_acc#5']).split(',') if r.strip()],
                        "isEnabled": True
                    }
                    ams_res = bot.ams.create_account(ams_payload)
                    if ams_res.get("ok"):
                        bot.my_bot.send_message(for_reports, f"✅ AMS: Аккаунт {ams_payload['email']} успешно создан в мастер-базе")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка создания: {ams_res.get('error')} | {ams_res.get('message')}")
                except Exception as e:
                    bot.my_bot.send_message(for_reports, f"💥 AMS Exception (create): {traceback.format_exc()}")

                bot.my_bot.send_message(login,'Новый аккаунт сохранен')
        elif comm=='reaccept':
            if bot.users.get(str(login),{'route':''})['route']=='change_acc#4':
                acc=bot.accs[bot.users[str(login)]['a']]
                caption=f"Изменение данных аккаунта {bot.users[str(login)]['a']}\n"
                if bot.users[str(login)]['data_acc#0']!='': caption+=f"{acc['Пароль']} -> {bot.users[str(login)]['data_acc#0']}\n"; acc['Пароль']=bot.users[str(login)]['data_acc#0']
                if bot.users[str(login)]['data_acc#0_1']!='': caption+=f"{acc['Почта']} -> {bot.users[str(login)]['data_acc#0_1']}\n"; acc['Почта']=bot.users[str(login)]['data_acc#0_1']
                if bot.users[str(login)]['data_acc#1']!='': caption+=f"{acc['Игры']} -> {bot.users[str(login)]['data_acc#1']}\n"; acc['Игры']=bot.users[str(login)]['data_acc#1']
                if bot.users[str(login)]['data_acc#1_1']!='': caption+=f"{acc['Резервные коды']} -> {bot.users[str(login)]['data_acc#1_1']}\n"; acc['Резервные коды']=bot.users[str(login)]['data_acc#1_1']
                if bot.users[str(login)]['data_acc#2']!='': caption+=f"{acc['Дополнительно']} -> {bot.users[str(login)]['data_acc#2']}\n"; acc['Дополнительно']=bot.users[str(login)]['data_acc#2']
                if bot.users[str(login)]['data_acc#3']!='': caption+=f"QR изменен\n"; acc['QR']=bot.users[str(login)]['data_acc#3']
                
                
                bot.users[str(login)]['route']=''
                bot.save_data()
                bot.my_bot.send_message(login,'Данные изменены')
                bot.batya_report(caption,login)
                bot.clean_expired_change(login)
                bot.add_new_change(login)

                try:
                    target_email = bot.users[str(login)]['data_acc#0_1'] if bot.users[str(login)]['data_acc#0_1'] else acc['Почта']
                    acc_info = bot.ams.get_account_id_by_email(target_email)
                    
                    if acc_info.get("ok"):
                        account_id = acc_info.get("accountId")
                        ams_update = {}
                        
                        if bot.users[str(login)]['data_acc#0']: ams_update["password"] = bot.users[str(login)]['data_acc#0']
                        if bot.users[str(login)]['data_acc#1']: ams_update["gameTitles"] = bot.users[str(login)]['data_acc#1'].split("\n")
                        if bot.users[str(login)]['data_acc#0_1']: ams_update["email"] = bot.users[str(login)]['data_acc#0_1']
                        if bot.users[str(login)]['data_acc#2']: ams_update["additionalInfo"] = [g.strip() for g in bot.users[str(login)]['data_acc#2'].split(',')]
                        if bot.users[str(login)]['data_acc#1_1']: ams_update["reserveCodes"] = [r.strip() for r in bot.users[str(login)]['data_acc#1_1'].split(',')]
                        
                        if ams_update:
                            upd_res = bot.ams.update_account(account_id, ams_update)
                            bot.my_bot.send_message(for_reports, f"🔄 отправка в AMS: {account_id}\n {ams_update}")
                            bot.my_bot.send_message(for_reports, f"🔄 ответ AMS: {upd_res}")
                            if upd_res.get("ok"):
                                bot.my_bot.send_message(for_reports, f"🔄 AMS: Аккаунт {target_email} обновлен")
                                bot.my_bot.send_message(login, f"🔄 AMS: Аккаунт {target_email} обновлен")
                            else:
                                bot.my_bot.send_message(for_reports, f"⚠️ AMS Ошибка обновления: {upd_res}")
                                bot.my_bot.send_message(login, f"⚠️ AMS Ошибка обновления: {upd_res}")
                    else:
                        bot.my_bot.send_message(for_reports, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления")
                        bot.my_bot.send_message(login, f"⚠️ AMS: Аккаунт с почтой {target_email} не найден в мастер-базе для обновления")
                except Exception as e:
                    bot.my_bot.send_message(for_reports, f"💥 AMS Exception (update): {traceback.format_exc()}")
                    bot.my_bot.send_message(login, f"💥 AMS Exception (update): {traceback.format_exc()}")
        elif comm=='days7':
            arr=['Срок аренды аккаунта '+bot.users[str(login)]['a']+' истекает. ID консоли и ник покупателя: '+bot.accs[bot.users[str(login)]['a']]['id_client'],
                 bot.accs[bot.users[str(login)]['a']]['id_client_time']+7*24*60*60,2]
            bot.alarms4t[bot.users[str(login)]['a']]=arr
            bot.save_data()
            bot.my_bot.send_message(login,'Вы получите уведомление через '+str(7-1)+' дней')
        elif comm=='days30':
            arr=['Срок аренды аккаунта '+bot.users[str(login)]['a']+' истекает. ID консоли и ник покупателя: '+bot.accs[bot.users[str(login)]['a']]['id_client'],
                 bot.accs[bot.users[str(login)]['a']]['id_client_time']+30*24*60*60,2]
            bot.alarms4t[bot.users[str(login)]['a']]=arr
            bot.save_data()
            bot.my_bot.send_message(login,'Вы получите уведомление через '+str(30-1)+' дней')
        elif comm=='daysoth':
            bot.users[str(login)]['route']='add_id2'
            bot.my_bot.send_message(login,'Введите количество дней, на которое аккаунт будет сдаваться в аренду (числом)')
            
    except Exception as e:
        bot.my_bot.send_message(for_reports,traceback.format_exc())
        
        bot.imt(callback.from_user.id,str(traceback.format_exc()))
        debag(traceback.format_exc())

@bot.my_bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.my_bot.get_file(message.document.file_id)
    downloaded_file = bot.my_bot.download_file(file_info.file_path)
    with open('received_file.json', 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        with open('received_file.json', 'r') as json_file:
            data = json.load(json_file)
            data=data['db']['entries']
            db=shelve.open(AU_CODE_DATA_SHELVE)
            for obj in data:
                db[obj['name']]=obj['info']['secret']
            db2=shelve.open(AU_CODE_HAND_DATA_SHELVE)
            for key in db2:
                db[key]=db2[key]
            db2.close()
            db.close()
            bot.my_bot.reply_to(message, "Файл успешно загружен и обработан!")

    
        try:
            tsv_data = bot.convert_shelve_to_tsv()
            if tsv_data:
                bot.my_bot.send_message(for_reports, f"📊 Сгенерировано {len(tsv_data.split(chr(10)))} строк TSV")
                bot.send_to_aegis(tsv_data)
            else:
                bot.my_bot.send_message(for_reports, "❌ Нет данных для отправки")
        except:
            pass
    except json.JSONDecodeError:
        bot.my_bot.reply_to(message, "Ошибка: полученный файл не является корректным JSON.")
    except Exception as e:
        bot.my_bot.reply_to(message, f"Произошла ошибка при обработке файла: {traceback.format_exc()}")
        debag(traceback.format_exc())






############################################

import threading
import time
import schedule
from datetime import datetime

# ========== ЗАДАЧИ С ИНТЕРВАЛОМ (секунды) ==========
INTERVAL_TASKS = {
   'adbot2_mail': 580,      # каждые 5 минут
   'adbot2_mail2': 45,      # каждые 5 минут
   "aegis": 600,
    "check_maks_tek": 15,
    "reload": 610,
}

# ========== ЗАДАЧИ ПО РАСПИСАНИЮ (время) ==========

SCHEDULED_TASKS = {
   # '16:00': 'wb_suchi',
}

# Хранилище для статуса выполнения дневных задач (чтобы не дублировать)
daily_tasks_done = {}

def run_scheduled_task(task_name):
    """Выполняет запланированную задачу"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запуск: {task_name}")
        
        if task_name == 'wb_worker':
            bot.wb_worker()
            
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Выполнено: {task_name}")
        
    except Exception as e:
        print(f"Ошибка в запланированной задаче {task_name}: {e}")

def setup_scheduled_jobs():
    """Настраивает все запланированные задачи"""
    for time_str, task_name in SCHEDULED_TASKS.items():
        # schedule использует format "HH:MM"
        getattr(schedule, 'every').day.at(time_str).do(run_scheduled_task, task_name)
        print(f"Запланировано: {task_name} в {time_str}")

def interval_worker():
    current_time = time.time()
    last_run = {task: current_time for task in INTERVAL_TASKS}
    
    while True:
        current_time = time.time()
        
        for task_name, interval in INTERVAL_TASKS.items():
            if current_time - last_run[task_name] >= interval:
                try:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Интервал: {task_name}")
                    
                    if task_name == 'adbot2_mail2':
                        bot.adbot2_mail()
                    if task_name == 'reload':
                        bot.reload()
                    if task_name == 'adbot2_mail':
                        bot.adbot2_mail()
                        bot.save_data()
                    elif task_name == 'aegis':
                        try:
                            tsv_data = bot.convert_shelve_to_tsv()
                            if tsv_data:
                                bot.my_bot.send_message(for_reports, f"📊 Сгенерировано {len(tsv_data.split(chr(10)))} строк TSV")
                                bot.send_to_aegis(tsv_data)
                            else:
                                bot.my_bot.send_message(for_reports, "❌ Нет данных для отправки")
                        except:
                            pass
                    elif task_name == "check_maks_tek":
                        bot.check_maks_tek()


                    last_run[task_name] = current_time
                except Exception as e:
                    print(f"Ошибка в {task_name}: {e}")
                    print(traceback.format_exc())
        
        time.sleep(1)  

def scheduled_worker():
    """Фоновый поток для запланированных задач"""
    while True:
        schedule.run_pending()
        time.sleep(1)


interval_thread = threading.Thread(target=interval_worker, daemon=True)
interval_thread.start()
print("✓ Интервальные задачи запущены")

setup_scheduled_jobs()
scheduled_thread = threading.Thread(target=scheduled_worker, daemon=True)
scheduled_thread.start()
print("✓ Запланированные задачи запущены")


bot.my_bot.polling(none_stop=True, interval=0)
