from django.shortcuts import render, redirect
from django.views import View
from django.http.response import HttpResponse
from collections import deque
from .services import ServiceType

# get custom services and make a line  TODO db support
line_of_cars = { service.code : deque() for service in ServiceType }
next_ticket_number = 1
# current ticket serving
currently_serving = None

class TicketView(View):
    def get(self, request, service_type, *args, **kwargs):
        global next_ticket_number

        target_service = ServiceType.get_by_code(service_type)
        if not target_service:
            return HttpResponse("Service not found", status=404)

        minutes_to_wait = 0
        # calculate priority
        for service in ServiceType:
            if service == target_service:
                break
            minutes_to_wait += len(line_of_cars[service.code]) * service.minutes
        # add up the current cat's queue time
        minutes_to_wait += len(line_of_cars[target_service.code]) * target_service.minutes

        # update the queue
        current_ticket_number = next_ticket_number
        line_of_cars[service_type].append(current_ticket_number)
        next_ticket_number += 1
        # fetch context
        context = {
            'ticket_number': current_ticket_number,
            'minutes_to_wait': minutes_to_wait
        }
        return render(request, 'tickets/ticket.html', context)


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')

# build menu from given services
class MenuView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'services': list(ServiceType)
        }
        return render(request, 'tickets/menu.html', context)

class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'oil_queue_len': len(line_of_cars[ServiceType.OIL.code]),
            'tires_queue_len': len(line_of_cars[ServiceType.TIRES.code]),
            'diagnostic_queue_len': len(line_of_cars[ServiceType.DIAGNOSTIC.code]),
        }
        return render(request, 'tickets/processing.html', context)
    def post(self, request, *args, **kwargs):
        global currently_serving
        if line_of_cars[ServiceType.OIL.code]:
            currently_serving = line_of_cars[ServiceType.OIL.code].popleft()
        elif line_of_cars[ServiceType.TIRES.code]:
            currently_serving = line_of_cars[ServiceType.TIRES.code].popleft()
        elif line_of_cars[ServiceType.DIAGNOSTIC.code]:
            currently_serving = line_of_cars[ServiceType.DIAGNOSTIC.code].popleft()
        else:
            currently_serving = None

        return redirect('/next')

class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', {'ticket_id': currently_serving})