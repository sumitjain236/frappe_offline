
import frappe
import json
from datetime import datetime


def string_to_ms(date_string):
    d = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return int(d.timestamp() * 1000)


@frappe.whitelist()
def get_doc_offline(doctype, name, last_modified=None):
    # 1. check the permission
    # 2. if permission is true proceed to next step
    # 3. else return None
    # 4. if last_modified is None return the doc
    # 5. else check the modified date of the doc and compare it with last_modified
    # 6. if modified date is greater than last_modified return the doc

    permission = frappe.has_permission(doctype, name)
    if permission:
        try:
            if last_modified == None:
                # print('inside if')
                return {'data': frappe.get_doc(doctype, name),
                        'error': None,
                        'should_delete': False
                        }
            else:
                print('inside else')

                modified = frappe.db.get_value(doctype, name, "modified")
                if string_to_ms(str(modified).split(".")[0]) > string_to_ms(str(last_modified).split(".")[0]):
                    # print('modified: ', modified)
                    # print('last_modified: ', last_modified)
                    # print('inside if 2')

                    return {'data': frappe.get_doc(doctype, name),
                            'error': None,
                            'should_delete': False
                            }
                else:
                    # print('inside else 2')
                    return {'data': None,
                            'error': None,
                            'should_delete': False
                            }
        except Exception as e:
            print(e)
            return {'data': None,
                    'error': e,
                    'should_delete': True
                    }

    else:
        return {'data': None,
                'error': frappe.PermissionError,
                'should_delete': True
                }


@frappe.whitelist()
def get_list_offline(doctype, args, last_fetch_count=None, last_modified=None):
    # 1. check the permission of the doctype if permission is true proceed to next step
    # 2. else return error
    # 3. if last_fetch_count is None return the list
    # 4. else check the count of the list and compare it with last_fetch_count if count is greater than last_fetch_count return the list
    # 5. else check the modified date of the list and compare it with last_modified if modified date is greater than last_modified return the list
    # 6. else return None

    permission = frappe.has_permission(doctype, '')
    if permission:
        try:

            args = json.loads(args)

            if last_fetch_count == None:

                return {'data': frappe.get_list(doctype, filters=args.get('filters'), fields=args.get('fields'), limit=args.get('limit'), limit_start=args.get('limit_start'), order_by=args.get('order_by')),
                        'error': None,
                        'should_delete': False
                        }
            else:

                count = frappe.db.count(doctype, filters=args.get('filters'))

                if int(count) != int(last_fetch_count):

                    return {'data': frappe.get_list(doctype, filters=args.get('filters'), fields=args.get('fields'), limit=args.get('limit'), limit_start=args.get('limit_start'), order_by=args.get('order_by')),
                            'error': None,
                            'should_delete': False
                            }
                else:

                    modified = frappe.get_list(doctype, filters=args.get('filters'), fields=[
                        'modified'], limit=1, order_by='modified desc')

                    if string_to_ms(str(modified[0].modified).split(".")[0]) > string_to_ms(str(last_modified).split(".")[0]):

                        return {'data': frappe.get_list(doctype, filters=args.get('filters'), fields=args.get('fields'), limit=args.get('limit'), limit_start=args.get('limit_start'), order_by=args.get('order_by')),
                                'error': None,
                                'should_delete': False
                                }
                    else:

                        return {'data': None,
                                'error': None,
                                'should_delete': False
                                }

        except Exception as e:

            print(e)
            return {'data': None,
                    'error': e,
                    'should_delete': True
                    }
    else:

        return {'data': None,
                'error': frappe.PermissionError,
                'should_delete': True
                }


# @frappe.whitelist()
# def get_call_offline(method, params, last_modified=None, user_last_modified=None):

#     try:
#         params = json.loads(params)
#         params = frappe._dict(params)
#         print(params)
#         if last_modified == None:
#             print('inside if')
#             # send param if its not empty
#             return {'data': frappe.call(method, params if params else None),
#                     'error': None,
#                     'should_delete': False
#                     }

#         else:
#             print('inside else')
#             if string_to_ms(str(user_last_modified).split(".")[0]) > string_to_ms(str(last_modified).split(".")[0]):
#                 print('inside if 2')
#                 return {'data': frappe.call(method, params),
#                         'error': None,
#                         'should_delete': False
#                         }
#             else:
#                 print('inside else 2')
#                 return {'data': None,
#                         'error': None,
#                         'should_delete': False
#                         }
#     except Exception as e:
#         print(e)
#         return {'data': None,
#                 'error': e,
#                 'should_delete': True
#                 }


# @ frappe.whitelist()
# def trial():
#     return frappe.get_doc('Indexdb', '30edbfa525')
