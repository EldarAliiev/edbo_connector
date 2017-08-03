#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import glob
import time
import pdfkit
import cups
from client import EDBOWebApiClient
from helper import EDBOWebApiHelper

export_directory = '/home/zim/requests'


def save_documents(documents_path_suffix):
    def wrapper(fn):
        def wrapped(*args):
            os.system('clear')

            documents_root = os.path.join(export_directory, documents_path_suffix)
            if not os.path.exists(documents_root):
                os.makedirs(documents_root)

            requests = EDBOWebApiClient.get_requests_list(full=True)
            requests_count = len(requests)

            for index, request in enumerate(requests, start=1):
                request_id = request['personRequestId']
                if request['personRequestStatusTypeId'] not in [3]:
                    document_filename = os.path.join(documents_root, '%d.jpg' % request_id)
                    if not os.path.exists(document_filename):
                        document_response = fn(request_id)
                        document_size = int(document_response.headers['Content-Length'])
                        if document_size > 1024:
                            with open(document_filename, 'wb') as file:
                                file.write(document_response.content)
                                print(
                                    '%d/%d: %d.jpg [%s]' % (
                                        index,
                                        requests_count,
                                        request_id,
                                        EDBOWebApiHelper.format_file_size(document_size)
                                    )
                                )
                        else:
                            print(u'Документ пустий')
                    else:
                        print(u'Документ вже існує')
                else:
                    print(u'%d/%d: Заяву №%d скасовано' % (index, requests_count, request_id))

        return wrapped

    return wrapper


class EDBOWebApiExport:
    @staticmethod
    def speciality_path(speciality_name):
        path = os.path.join(export_directory, speciality_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def directory_size(directory):
        return len(os.listdir(directory))

    @staticmethod
    def get_business_code(speciality_code):
        return {
            '222': u'М',
            '228': u'П',
            '225': u'МП',
            '221': u'С',
            '226': u'Ф',
        }.get(speciality_code, None)

    @staticmethod
    def business_exists(speciality_path, person_id):
        return len(glob.glob(os.path.join(speciality_path, '* (%d)' % person_id))) > 0

    @staticmethod
    def all(filename):
        output_file = os.path.join(export_directory, filename)
        with open(output_file, 'w', encoding='utf8') as f:
            f.write(
                json.dumps(
                    EDBOWebApiClient.get_full_requests(),
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': '),
                    ensure_ascii=False
                )
            )
        return output_file

    @staticmethod
    def grouped():
        for request_id in EDBOWebApiClient.get_requests_list(15):
            request = EDBOWebApiClient.get_full_request(request_id)
            speciality_path = EDBOWebApiExport.speciality_path(request['specSpecialityAllCode'])

            if not EDBOWebApiExport.business_exists(speciality_path, request['personId']):
                business_code = EDBOWebApiExport.get_business_code(request['specialityCode'])
                business_number = EDBOWebApiExport.directory_size(speciality_path) + 1

                person_business = '%s%d %s (%d)' % (
                    business_code,
                    business_number,
                    request['fio'],
                    request['personId']
                )

                person_business_path = os.path.join(speciality_path, person_business)
                os.mkdir(person_business_path)

                person_data_path = os.path.join(person_business_path, 'export.json')
                print(person_data_path)
                print(u'Створення особової справи "%s"' % person_business)
            else:
                print(
                    u'Особова справа для "%s (%d)" існує!' % (
                        request['fio'],
                        request['personId']
                    )
                )

    @staticmethod
    @save_documents('Документи/Атестати')
    def get_all_atestats(person_request_id=None):
        return EDBOWebApiClient.get_atestat_image(person_request_id)

    @staticmethod
    @save_documents('Документи/Довідки')
    def get_all_regsk(person_request_id=None):
        return EDBOWebApiClient.get_regsk_image(person_request_id)

    @staticmethod
    def render_request_document(person_request, codeOfBusiness=None):
        if len(person_request['requestSubjectsResults']) == 4:
            person_request['requestSubjectsResults'] = sorted(person_request['requestSubjectsResults'], key=lambda k: k['subjectId'])

        rendered_document = EDBOWebApiHelper.render_document('templates/request.html', {'request': person_request, 'codeOfBusiness': codeOfBusiness})

        filename = os.path.join(export_directory, 'Документи', 'Заяви')
        if not os.path.exists(filename):
            os.makedirs(filename)

        filename = os.path.join(filename, '%d.pdf' % person_request['personRequestId'])

        pdfkit.from_string(
            rendered_document,
            filename,
            options={
                'page-size': 'A4',
                'margin-top': '0.10in',
                'margin-right': '0.25in',
                'margin-bottom': '0.15in',
                'margin-left': '0.25in',
            }
        )
        #with open(filename, 'w') as f:
        #    f.write(rendered_document)

    @staticmethod
    def gen_work_table():
        import json
        with open('full.json', 'r') as f:
            data = json.load(f)
            data = sorted(data, key=lambda k: k['dateCreate'])
            table_code = EDBOWebApiHelper.render_document('templates/work_table.html', {'requests': data})
            with open('work_table.html', 'w') as out:
                out.write(table_code)

    @staticmethod
    def render_all_requests_documents():
        with open('full.json', 'r') as f:
            data = json.load(f)
            data = sorted(data, key=lambda k: k['dateCreate'])
            for index, request in enumerate(data, start=1):
                if request['personRequestStatusTypeId'] != 3:
                    EDBOWebApiExport.render_request_document(request, '%dм' % index)
                    print('%d/%d OK' % (index, len(data)))

    @staticmethod
    def print_document(file):
        cups_connection = cups.Connection()
        printers_list = cups_connection.getPrinters()
        if len(printers_list) > 0:
            printer_name, printer_info = list(printers_list.items())[0]
            print(u'Старт друку документу "%s" на "%s"' % (file, printer_name))
            cups_connection.printFile(
                'Hewlett-Packard-HP-LaserJet-P3010-Series',
                file,
                u'Друкування документу "%s" на "%s"' % (file, printer_name),
                options={}
            )
            print(u'Документ "%s" роздруковано на "%s"' % (file, printer_name))
        else:
            print(u'Не знайдено жодного доступного принтеру')

    @staticmethod
    def print_all_requests(print_timeout=0):
        with open('full.json', 'r') as f:
            data = json.load(f)
            data = sorted(data, key=lambda k: k['dateCreate'])
            document_root = os.path.join(export_directory, 'Документи')
            for index, request in enumerate(data, start=0):
                print(request['personRequestId'])
                if request['personRequestStatusTypeId'] != 3 and request['specialityCode'] == '226' and\
                                request['educationFormName'] == 'Заочна' and request['personRequestId'] >= 3475487:
                    documents_package = [
                        os.path.join(document_root, 'Заяви', '%d.pdf' % request['personRequestId']),
                        os.path.join(document_root, 'Атестати', '%d.jpg' % request['personRequestId']),
                        os.path.join(document_root, 'Довідки', '%d.jpg' % request['personRequestId'])
                    ]

                    for document in documents_package:
                        if os.path.exists(document):
                            EDBOWebApiExport.print_document(document)

                    print('%d/%d OK' % (index, len(data)))
                    time.sleep(print_timeout)

cups_connection = cups.Connection()
for job_id, info in cups_connection.getJobs().items():
    cups_connection.cancelJob(job_id)

# EDBOWebApiExport.all('full.json')
# EDBOWebApiExport.get_all_regsk()
# EDBOWebApiExport.render_all_requests_documents()
# EDBOWebApiExport.gen_work_table()

# EDBOWebApiExport.print_all_requests(10)
# EDBOWebApiExport.get_all_atestats()
