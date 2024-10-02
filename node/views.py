from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from .forms import NodeCreationForm, NodeMotorCreationForm
from .models import Node, NodeMotor
from work_tower.models import WorkTowerLevel


def nodes_list_view(request):
    nodes = Node.objects.all()
    return render(request, 'node/nodes_list.html', {'nodes': nodes})


def motors_list_view(request):      # tested
    """
    Displays a paginated list of NodeMotor instances. If an error occurs while
    fetching motors or pagination fails, the error is handled gracefully.
    
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
                               about the request, including the 'page' query parameter.
    
    Returns:
        HttpResponse: The rendered 'motors_list.html' template displaying the paginated
                      list of motors and pagination controls, or an error message.
    """
    try:
        motors = NodeMotor.objects.all()
        paginator = Paginator(motors, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except (PageNotAnInteger, EmptyPage):  
        page_obj = paginator.page(1)

    except NodeMotor.DoesNotExist:
        page_obj = None

    context = {
        'motors': motors,
        'page_obj': page_obj,
    }
    return render(request, 'node/motors_list.html', context)



def create_node_motor_view(request):    
    """
    Handles the creation of a new NodeMotor instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata and form data.

    Returns:
        HttpResponse: The rendered template with the form for GET requests, or a redirect 
                      to the 'node:create_node' URL after a successful form submission.
    """
    if request.method == 'POST':
        form = NodeMotorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:show_created_node_motor')  
        else:
            print(form.errors)
    else:
        form = NodeMotorCreationForm()
    
    return render(request, 'node/create_node_motor.html', {'form': form})


def create_node_view(request):      
    """
    Handles the creation of a new Node instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata and form data.

    Returns:
        HttpResponse: The rendered template with the form for GET requests, or a redirect 
                      to the 'node:node_list' URL after a successful form submission.
    """
    if request.method == 'POST':
        form = NodeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('node:show_created_node')  
    else:
        form = NodeCreationForm()

    return render(request, 'node/create_node.html', {'form': form})


def show_created_node_motor_view(request):  
    """
    Displays a success message after a successful NodeMotor creation.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the success message or an appropriate message.
    """
    last_node_motor = NodeMotor.objects.last()
    
    if last_node_motor is None:
        message = "Двигун не був створений."
    else:
        message = ""  

    return render(request, 'node/show_created_node_motor.html', {
        'last_node_motor': last_node_motor,
        'message': message
    })


def show_created_node_view(request):        
    """
    Displays a success message after a successful Node creation.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the success message.
    """

    last_node = Node.objects.last()
    return render(request, 'node/show_created_node.html', {'last_node': last_node})


def node_detail_view(request, node_id):     
    """
    Displays the details of a specific Node instance.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        node_id (int): The ID of the Node instance to be retrieved.

    Returns:
        HttpResponse: The rendered template displaying the details of the Node and its 
                      associated NodeMotor.
    """
    
    node = get_object_or_404(Node, id=node_id)
    motor = node.motor

    context = {
        'node': node,
        'motor': motor
    }
    return render(request, 'node/node_detail.html', context)


def search_node_view(request):      
    """
    View to search for a Node instance by its index and display its information.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the details of the Node.
    """
    if request.method == 'POST':
        index = request.POST.get('index')

        if not index:
            return render(
                request, 
                'node/search_node_form.html', 
                {'error': 'Введіть, буль ласка, індекс.'}
                )

        try:
            node = Node.objects.get(index=index)
            motor = node.motor
            return render(
                request, 
                'node/search_node_form.html', 
                {'node': node, 'motor': motor,}
                )

        except Node.DoesNotExist:
            return render(
                request, 
                'node/search_node_form.html', 
                {'error': f'Вузол з індексом "{index}" не знайдено.'}
                )

    return render(request, 'node/search_node_form.html')


def get_level_nodes_view(request):      
    """
    Displays a list of Node instances filtered by the selected WorkTowerLevel.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered 'nodes_by_level.html' template displaying the filtered nodes.
    """
    nodes = None
    selected_level = None
    error = None

    if request.method == 'POST':
        level_id = request.POST.get('level')
        if not level_id: 
            error = 'Введіть, буль ласка, відмітку.'
        else:
            try:
                selected_level = get_object_or_404(WorkTowerLevel, id=level_id)
                nodes = Node.objects.filter(level=selected_level)

                if not nodes.exists():  
                    error = f'На відмітці "{selected_level.level}" вузлів немає.'

            except WorkTowerLevel.DoesNotExist:
                error = f'Рівень відмітки "{level_id}" не знайдено.'

    levels = WorkTowerLevel.objects.all()

    context = {
        'levels': levels,
        'nodes': nodes,
        'selected_level': selected_level,
        'error': error,  
    }

    return render(request, 'node/level_nodes.html', context)



def pre_change_data_view(request):      
    """
    Displays the endpoints to change the data of the NodeMotor and Node instances.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the buttons to change the data in database.
    """

    return render(request, 'node/pre_change_data.html',)


def update_node_motor_view(request):        
    """
    Handles the NodeMotor instance updating with the provided form data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered template displaying the updated details of the NodeMotor.
    """
    if request.method == 'POST':
        power = request.POST.get('power')
        
        if not power:
            return render(
                request, 
                'node/update_motor_form.html', 
                {'error': 'Введіть, буль ласка, потужність.'}
                )
        try:
            power = float(power)
            motor_id = request.POST.get('motor_id')

            if 'update' in request.POST:
                try:
                    motor = NodeMotor.objects.get(id=motor_id)
                except NodeMotor.DoesNotExist:
                    return render(
                        request, 
                        'node/update_motor_form.html', 
                        {'error': f'Двигун з ID {motor_id} не знайдено.'},
                        )
                
                form = NodeMotorCreationForm(request.POST, instance=motor)
                if form.is_valid():
                    form.save()
                    return redirect('node:updated_motor_message')
                else:
                    return render(
                        request, 
                        'node/update_motor_form.html', 
                        {'form': form, 'motor': motor},
                        )

            motor = NodeMotor.objects.filter(power=power).first()
            if motor is None:
                return render(
                    request, 
                    'node/update_motor_form.html', 
                    {'error': f'Не знайдено двигун з потужністю {power}.'},
                    )

            form = NodeMotorCreationForm(instance=motor)
            return render(
                request, 
                'node/update_motor_form.html', 
                {'form': form, 'motor': motor},
                )

        except ValueError:
            return render(
                request, 
                'node/update_motor_form.html', 
                {'error': 'Не правильний ввід. Введіть, буль ласка, числове значення.'},
                )

    return render(request, 'node/update_motor_form.html')


def update_node_view(request):         
    """
    Handles the Node instance update based on the entered index.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template displaying the form to update the Node.
    """
    
    if request.method == 'POST':
        index = request.POST.get('index')
        
        if not index:
            return render(
                request, 
                'node/update_node_form.html', 
                {'error': 'Введіть, буль ласка, індекс.'}
            )

        try:
            node = Node.objects.get(index=index)

            if 'update' in request.POST:
                form = NodeCreationForm(request.POST, instance=node)
                if form.is_valid():
                    form.save()
                    return redirect('node:updated_node_message') 
            else:
                form = NodeCreationForm(instance=node)

            return render(
                request, 
                'node/update_node_form.html', 
                {'form': form, 'node': node}
            )
        except Node.DoesNotExist:
            return render(
                request, 
                'node/update_node_form.html', 
                {'error': f'Вузол з індексом "{index}" не знайдено.'}
            )
    return render(request, 'node/update_node_form.html')


def delete_motor_view(request):
    """
    View to delete a NodeMotor instance based on the entered power value.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with the form for inputting power and feedback after deletion.
    """
    if request.method == 'POST':
        power = request.POST.get('power')

        if not power:
            return render(
                request, 
                'node/delete_node_motor.html', 
                {'error': 'Введіть значення потужності двигуна.'}
            )

        try:
            power = float(power)
            motor = NodeMotor.objects.get(power=power)
            motor.delete()
            return redirect('node:deleted_motor_message')
            
        except NodeMotor.DoesNotExist:
            return render(
                request, 
                'node/delete_node_motor.html', 
                {'error': f'Не знайдено двигун потужністю {power}кВт.'}
            )
        except ValueError:
            return render(
                request, 
                'node/delete_node_motor.html', 
                {'error': 'Невірний ввід. Введіть числове значення потужності.'}
            )
        except ProtectedError:
            return render(
                request, 
                'node/delete_node_motor.html', 
                {'error': 'Видалення даного двигуна заборонено, оскільки він використовується щонайменше на одному вузлі.'}
            )

    return render(request, 'node/delete_node_motor.html')


def delete_node_view(request):
    """
    View to delete a Node instance based on the entered index.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template with the form for inputting index and feedback after deletion.
    """
    if request.method == 'POST':
        index = request.POST.get('index')

        if not index:
            return render(
                request, 
                'node/delete_node.html', 
                {'error': 'Введіть, буль ласка, індекс.'}
            )

        try:
            node = Node.objects.get(index=index)
            node.delete()
            return redirect('node:deleted_node_message')
            
        except Node.DoesNotExist:
            return render(
                request, 
                'node/delete_node.html', 
                {'error': f'Вузол з індексом "{index}" не знайдено.'}
            )

    return render(request, 'node/delete_node.html')
