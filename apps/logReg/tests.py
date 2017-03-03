from django.test import TestCase

# Create your tests here.
def destination(request, id):
    location = Travel.objects.get(id=id)
    others = User.objects.filter(travelplan__the_travel=location).exclude(travel__travelplan__the_user_id=location.creator.id)
    # others = others.exclude(travel__travelplan__the_user_id=location.creator.id)
    context = {
        'others': others,
        'users': User.objects.get(id=request.session['id']),
        'location': location,
    }
    return render(request, 'logReg/users.html', context)


def add(request):
    if request.method == 'GET':
        return render(request, 'logReg/add.html')

def join(request, id):
    # if request.method == 'POST':
        traveling = Travel.objects.get(id=id)
        user = User.objects.get(id=request.session['id'])
        TravelPlan.objects.create(the_user=user, the_travel=traveling)
        return redirect('/pokes')


class Travel(models.Model):
    destination = models.CharField(max_length=45, null=True, blank=True)
    creator = models.ForeignKey(User, related_name='travel', blank=True, null=True)
    description = models.CharField(max_length=45, null=True, blank=True)
    travel_start = models.DateTimeField(auto_now=False, auto_now_add=False, default='9999-11-29', null=True, blank=True)
    travel_end = models.DateTimeField(auto_now=False, auto_now_add=False, default='9999-11-29', null=True, blank=True)
    objects = Umanager()
tp = TravelPlan.objects.all()
        going_id = []
        going = []
        for x in tp:
            if x.the_user.id == request.session['id']:
                going.append(x)
                going_id.append(x.the_travel_id)
        travel = travel.exclude(id__in=going_id)
# travel = Travel.objects.create(destination=request.POST['dest'], description=request.POST['desc'], travel_start=request.POST['date_from'], travel_end=request.POST['date_to'], creator=user)
        # TravelPlan.objects.create(the_travel=travel, the_user=user)
</table>
<h4>Other user's travel plans</h4>
<table>
<thead>
    <tr>
        <th>Destination</th>
        <th>Travel-Start Date</th>
        <th>Travel-End Date</th>
        <th>Description</th>
        <th>Do You Want to Join?</th>
    </tr>
</thead>
<tbody>
{% for x in travel %}
    <tr>
        <td><a href="/destination/{{ x.id }}">{{ x.destination }}</a></td>
        <td>{{ x.travel_start|date:"M d Y" }}</td>
        <td>{{ x.travel_end|date:"M d Y" }}</td>
        <td>{{ x.description }}</td>
        <td><a href="/join/{{ x.id }}">Join</a></td>
    </tr>
{% endfor %}
</tbody>
</table>
<h4><a href="/add">Add travel plan</a></h4>


<h4>People you may want to poke:</h4>
<table>
<thead>
    <tr>
        <th>Name</th>
        <th>Alias</th>
        <th>Email Address</th>
        <th>Poke History</th>
        <th>Action</th>
    </tr>
    </thead>
    <tbody>
    {% for people in pokes %}
        <tr>
            <td>{{ people.pokee.name }}</td>
            <td>{{ people.pokee.alias }}</td>
            <td>{{ people.pokee.email }}</td>
            <td>{{ people.poke_count}}</td>
            <td><form action="/add_poke/{{ people.pokee.id }}" method="post">
                {% csrf_token %}
                <input type="submit" name="poke" value="Poke!">
            </form></td>
        </tr>
    {% endfor %}
    {% for people in peoples %}
        <tr>
            <td>{{ people.name }}</td>
            <td>{{ people.alias }}</td>
            <td>{{ people.email }}</td>
            <td>0</td>
            <td><form action="/add_poke/{{ people.id }}" method="post">
                {% csrf_token %}
                <input type="submit" name="poke" value="Poke!">
            </form></td>
        </tr>
    {% endfor %}
</table>
# if Poke.objects.filter(poker_id=user.id, pokee_id=id).exists():
#     counter = Poke.objects.get(poker_id=user.id, pokee_id=id)
#     counter.poke_count = F('poke_count') + 1
#     counter.save()
#     return redirect('/quotes')
# else:
#     Poke.objects.create(poker_id=user.id, poke_count=1, pokee_id=id)