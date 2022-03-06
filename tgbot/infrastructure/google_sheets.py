import datetime
import logging
from dataclasses import dataclass

import gspread_asyncio
from gspread_asyncio import AsyncioGspreadClient


async def create_spreadsheet(client: AsyncioGspreadClient, spreadsheet_name: str):
    spreadsheet = await client.create(spreadsheet_name)
    spreadsheet = await client.open_by_key(spreadsheet.id)
    return spreadsheet


async def add_worksheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet,
                        worksheet_name: str):
    try:
        return await async_spreadsheet.worksheet(worksheet_name)
    except Exception as e:
        logging.error(e)


async def share_spreadsheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet,
                            email: str, role: str = 'writer', perm_type: str = 'user'):
    await async_spreadsheet.share(email, perm_type=perm_type, role=role)


@dataclass
class ExcelForm:
    phone_number: str
    full_name: str
    address: str
    geolocation: str
    description: str
    photo: str
    urgent_status: str
    comment: str
    time: datetime.datetime

    COLUMNS = ['phone_number', 'full_name', 'address', 'geolocation',
               'description', 'time', 'urgent_status', 'photo', 'comment']

    def create_row(self):
        return [
            str(getattr(self, row_name, '-') or '-')
            for row_name in self.COLUMNS
        ]


async def write_to_sheet(google_client, excel_form: ExcelForm, sheet_id):
    async_spreadsheet = await google_client.open_by_key(sheet_id)
    worksheet = await add_worksheet(async_spreadsheet, 'Заяви')
    await worksheet.append_row(excel_form.create_row())
