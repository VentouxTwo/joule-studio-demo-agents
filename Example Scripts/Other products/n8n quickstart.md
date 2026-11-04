hey I'm Max the original flowgrammer and welcome  to your n8n quick start i'm going to teach you the  
0:06
key fundamentals to building any n8n workflow that  includes triggers and actions how items of data  
0:12
work between steps in your n8n workflows how to  map data between those steps and transform it and  
0:19
route it based on business logic i'm also going to  teach you how to connect to apps and services so  
0:23
you can perform actions in those apps and services  in your app stack and we're going to do this all  
0:27
with a super simple workflow it's an installation  request so there'll be a web form and it'll send a  
0:34
notification to Slack it's a simple workflow to  teach you the key fundamentals of N8N that you  
0:38
can leverage in your actual use cases and if you  came here wanting to build some fancy AI stuff I  
0:44
hear you it's very exciting there's a lot of hype  about it right now but I strongly recommend that  
0:47
you watch this video first learn these foundations  and then jump off into that agentic future all  
0:53
right with all that in mind let's switch to N8N  and begin i'm here in a brand new n8n workspace  
Set up Form Trigger
1:00
and let's start a new workflow from scratch this  is going to take us to the workflow canvas this is  
1:05
where you build out your workflow activate it and  then it runs automatically it saves you a bunch of  
1:08
time let's add our first step to the workflow and  that's going to be a workflow trigger in Nen we  
1:13
have triggers that kick off workflows and then we  have actions that perform steps in your workflow  
1:17
there's lots of different types of triggers that  you can leverage for example if you want to kick  
1:21
off the workflow based on an event in an app or  service that you use in your app stack you can  
1:25
go on to on app event if you're building an AI  chatbot perhaps you're going to start off with  
1:29
our chat trigger since today we're creating a  web form automation let's start off with an on  
1:34
form submission cuz n8n is going to give us a web  form that we can give to the end user to fill out  
1:38
to kick off the workflow let's click to add that  to the canvas this added the node to the canvas  
1:43
by default the trigger node the form trigger and  we can see that it's a trigger node because it's  
1:47
got this lightning bolt on it and if I hover near  it it gets its own execute workflow button let's  
1:51
go ahead and set it up there's various parameters  that you need to fill out before you can execute a  
1:57
step these are required fields as you can see here  there's an error around the form title so let's go  
2:01
ahead and give it a title request an installation  and let's also give it a description fill out this  
2:06
form to request an installation we'll reach out  via email to finalize your appointment next let's  
2:10
add the form fields that we want the users to  actually fill out these are called form elements  
2:14
in n8n let's add the first one and let's ask for  the email and since an email is text we could keep  
2:20
this to text but we do have a specific email type  and this offers a bit extra data validation when  
2:25
the user fills that out if they get the email  wrong so let's add that and we won't add a  
2:28
placeholder for now but let's make it required and  then let's also capture their preferred install  
2:33
date so we can do a bit of conditional routing  based on that and I can show you how to work with  
2:37
data and manipulate it in n8n as well and let's  set that to a date because then it'll be a nice  
2:43
little date picker for the user to use for now  let's respond when the form is submitted so it'll  
2:47
just say "Hey great your form was submitted." But  in future you could make this a multi-step form  
2:51
if you're evolving this now that I filled out the  parameters of my node the next thing is we need to  
2:55
test it and we do that by clicking execute step in  the case of the form trigger this pops up a test  
3:01
form this is what your end user is going to see  once you activate the workflow let's go ahead and  
3:05
fill that out name.com let's say my preferred  install date i need this in two days like I'm  
3:10
really busy i got to get this stuff installed so  I submit that okay let's go ahead and close that  
3:14
popup and we can see that it executed successfully  and there's a green check mark in my output here  
Output data and n8n items
3:18
and I have some output data here as well how nodes  work in n8n be it a trigger or an action is they  
3:24
run their step and then they output some data and  that's what we can see here in the output there's  
3:28
a few different ways to visualize that data  for example I'm looking in JSON mode right now  
3:32
because most of this data does get passed in JSON  format in n8n so this is a rather true to form  
3:37
representation of that data i can also see it as  a table if that's useful for the type of data I'm  
3:42
looking at and there's also a schema view which  extrapolates the schema of this data and shows  
3:46
it in a format where if I had nesting I could also  collapse it this would be a good juncture in time  
3:51
to talk about n items what they are and how to  work with them so as you can see we have one item  
3:56
of data in my output and if I go to my workflow  we can see the node executed successfully it's  
4:00
got a green check and there's an item of data  coming out of that as well what is an item of  
4:04
data basically each node in nin8nn including this  trigger node outputs an array of items that's its  
4:10
payload that it sends out that you can pipe in to  the next step now the one contract between nodes  
4:16
in n8n is that they always need to pass along this  array and it should have zero to many items in  
4:21
this case we have one item of data in here because  there's one element in this top level array which  
4:25
is why there's one item here that's going to  be useful for you to know because most nodes  
4:29
perform their step on each item of data and a lot  of folks sometimes get the looping paradigm wrong  
4:34
and try to add looping steps when they don't need  to because again nodes perform each step on each  
4:39
incoming item of data that will become clearer in  the next step when we add some conditional routing  
Pinning output data
4:44
before we continue though if I continue to test  my workflow be it from this execute step button  
4:48
here or execute workflow button here i'm going  to continue seeing that popup and I'm going to  
4:52
have to fill it out now in our web form that's not  too bad there's just two form fields but what if  
4:57
it's a subscription event for Stripe or something  that's difficult to replicate for my main system  
5:01
it's going to be really annoying to basically keep  creating test data as I do that so what you can do  
5:05
is pin the data in this node so each time that we  run it it just outputs the pinned data to do that  
5:11
we can hit this pin data button here this data  is now pinned we can see that visualized in the  
5:16
canvas as well so each time I mash this execute  workflow button it doesn't actually run it just  
5:20
outputs whatever payload was sitting in there  super useful pro tip that I highly recommend  
5:24
with pin data once I activate my workflow it  won't be used on those production executions  
5:29
but it will stay here for when I come back here  for a future session when I maybe want to test my  
Add conditional logic
5:33
flow let's now add some conditional routing logic  that routes it to Slack if the preferred install  
5:37
date is within 7 days and otherwise continues the  workflow to do that I'll click the plus button  
5:42
here and since I want some conditional routing  we need to go into the flow section of my nodes  
5:47
panel and here there's various things that can  control the flow what we need here is an if node  
5:51
if you do need to have multiple output branches  depending on more complex conditional logic you  
5:57
could also opt for the switch node in this case  we're just checking if it's under 7 days away so  
6:01
we can use the if node and I'll drag and drop that  onto the canvas just to contextualize this we can  
6:06
now see I've got my pin trigger sending one item  of data into my if node if I open it up I can see  
6:11
that I've got the one item of data flowing into  here and in the if node it also has parameters  
6:17
that we set up to inform how the step runs and we  do this by setting up one or many conditions that  
6:22
we evaluate and they might evaluate to true or  false and they'll go out the true branch or the  
6:27
false branch let's set up the first condition to  do that we want to check if the preferred install  
6:33
date is 7 days into the future of right now or  not so we can actually drag and drop that onto  
Mapping and transforming data
6:38
this value and this turns it to an expression in  n before it was set to fixed that's the default  
6:43
so it just treats this as text which I can also  type but if it's set to an expression anything  
6:47
within these curly brackets will be treated as  an expression that is evaluated and we can see  
6:52
the evaluated result here is that date so I can  drag and drop data from previous nodes and map  
6:58
them into the steps for current nodes to inform  the current step right so the next thing that  
7:02
we need to do is the operation that we want to  evaluate basically value one to value two right  
7:08
since this is a datetime we do have date and time  operators which is useful because dealing with  
7:13
date and times can be a little clunky mentally and  so this kind of helps make sure that you got sound  
7:18
logic for that so let's set this to is before or  equal to and we're going to get an error because  
7:23
we don't have anything set in the second value  yet but for the second value how to think of this  
7:27
i have a date we don't know what time it is and  we want to check if it's younger than 7 days from  
7:33
now so we got to get the now and add seven to it  right to do that we can set an expression go ahead  
7:39
and set an expression there and I'll do two open  brackets and in here I see an autocomplete shows  
7:45
up and in nan we do have a helper function to get  the time right now it's called dollar now so let's  
7:52
click to add that and we can see it's printed  a date time but we want now plus 7 days so if I  
7:57
hit period I can access autocomplete and see the  various helper methods that I can use if you're  
8:03
familiar with JavaScript this is also JavaScript  so you can apply JavaScript methods here as well  
8:07
but the Nadin team has a bunch of helper methods  in addition to JavaScript for the things that  
8:11
uh JavaScript might not cover let's add the  plus method and we can see here there's a  
8:16
mini documentation on how to use it we need to  specify the an integer on how much to increment  
8:20
the current datetime and the units to do that by  so days so actually we need exactly what's in this  
8:25
example so let's click to add that and then in  here let's write seven days and we can see that  
8:32
is now 7 days in the future if we run this it  does work because this gets cast to a date even  
8:40
though this is currently a text as you can see  there's a little a character there to make this a  
8:43
bit more robust and just to show the different  methods at work I can again hit a period here  
8:47
to access this autocomplete and there is a two  datetime method available here there's a bunch  
8:51
of others that you can look at as you're going  through your use case but this one makes it just  
8:55
a little bit more robust so now we're comparing a  datetime to a datetime let's test that it's true  
9:01
that's great we could test this again make sure  the logic's working because we set a date 2 days  
9:05
in advance so this should go to the false branch  that's working correctly we'll set that back great  
9:10
so now we've got conditional logic we're routing  to the true branch and we can see that's coming  
9:15
out there now before we add the slack node let's  annotate our workflow so it's a little clearer  
9:20
when we come back and we can do that by actually  modifying the name of this if node let's say is  
9:26
within 7 days it's a little tip I like to do for  my conditional nodes is phrase it as a question  
9:31
so it's kind of clear what the true condition  means versus the false condition and before we  
9:35
add the slack step for the false branch just for  completeness let's actually add a no operation  
9:39
node now as the name implies the no operation  node doesn't really do anything but it can be  
9:45
renamed for example there's a few more advanced  use cases for it but right now we're just going  
9:51
to use it as a placeholder so it's clear later in  the flow if we want to evolve that on to the Slack  
Set up Slack node
9:55
step let's click the plus from the true branch  because if it's within 7 days we want to send a  
9:59
Slack notification to someone on the team that's  going to be within action in an app i can also  
10:04
just search for it from here but just so you see  where that is in the app I would go into action  
10:08
in app i could scroll down to find it or again  just search inline here let's click on Slack now  
10:13
there's a lot of different actions in Slack again  I could search for that but what we're looking for  
10:16
is to send a message and so I'm going to click on  this send a message action here and it's connected  
10:22
to my workflow we can just confirm that by going  back to the canvas and seeing that's going to the  
10:26
true branch now we just need to set up the slack  step for most app nodes you are going to have to  
10:30
set a credential for it this is an entity within  edit end when you add your API key or whatever  
10:35
that service expects and then niten can connect to  that service on your behalf i have already created  
10:39
a slack credential for my Slack but you can create  a new one in line from here as well you're going  
10:44
to see this screen here if you're on NADN cloud  I do recommend the oorthth route because you get  
10:48
the fancy just click to connect experience you  go through the Slack popup and it auto connects  
10:52
otherwise you are going to have to go create an  access token but if you're stuck on that you can  
10:56
open the edit in docs to do that and you can also  rename your credential as well i'll use one that I  
11:01
already created but that is going to be the first  step now the resource and operation is already  
11:04
set cuz we picked that from the nodes panel so  we're sending a message now we need to pick who  
11:09
we send this message to right so let's drop down  here and let's send this to a channel and in this  
11:13
case let's pick from a list although I could also  set this by ID again there's an expression here  
11:18
that could be a dynamic thing in a more advanced  workflow in future so let's go ahead and select a  
11:23
channel let's send it to the sales channel and  let's do a simple text message but you could  
11:28
use Slack blocks in future that's what's going to  allow you to have buttons and all manner of those  
11:32
sorts of things and for the message text let's set  this to an expression and let's actually open this  
11:37
up so I can see a bit of a bigger view and I'm  going to paste in the static text that I would  
11:42
like so new install request within 7 days contact  email preferred install day and again here we're  
11:47
just going to drag and drop values from earlier in  my workflow the most recent node is autoexpanded  
11:52
but I could also map values from previous nodes  as well in this case they're the same because  
11:56
the conditional node doesn't manipulate data  it just routes it so let's go ahead and get  
12:00
that preferred install date and map that here as  well now again here I could combine these texts  
12:05
i could I write a lot more but you get the idea  i can combine static and dynamic text to send a  
12:10
useful notification all right let's test this by  running it we got a success check which means it  
12:16
worked let's go over to Slack and confirm that and  great we can see that came in here contact email  
12:21
name and email automated with this end workflow  perfect we can open up that workflow if ever need  
12:26
to troubleshoot future let's run that one more  time just to be sure worked again here and now  
12:30
we see two here perfecto next let's go back to  my workflow canvas and before we get too excited  
12:37
let's save our workflow now that the workflow  is saved if we leave this it's not going to work  
12:42
automatically yet because we haven't activated  the workflow so far we've run a test execution  
12:48
we've done a test form but we need to activate the  workflow and then as the workflow runs executions  
12:54
are going to occur in the execution tab of this  workflow so you can see there's a bunch of these  
12:58
test workflows that we just ran signified by this  beaker icon here and if I take that production URL  
13:04
from the web form so if I go in here I copy that  and in a new tab I enter that i can see the form  
13:10
is now live and if I fill this out let's do  a different one let's say max at company code  
13:15
and let's pick an install date also pretty soon  and submit that we can see firstly that that ran  
13:24
really quickly that's very cool but then if I go  into my workflow into executions I can see I have  
13:29
an execution that came in that doesn't have this  beaker icon this is a production execution i can  
13:33
go in here i can inspect that i can understand  if it failed perhaps or if I want to update the  
13:39
logic and one last thing to point out a little  pro tip before you go is that I can copy this  
13:44
into the editor this is going to unpin the current  data that I have repin the data from that current  
13:48
execution and now I could continue building  with that latest production execution which  
13:52
is super useful if you're troubleshooting or if  you're just evolving your workflow wow you did  
14:00
it good for you i hope you found this video  helpful you're well on your way to becoming  
14:04
a flowgrammer if you keep it up there's a ton of  resources in our global community to help you on  
14:09
your journey as you learn the first place you're  probably going to want to go is community.n.io  
14:14
that's our official community forums where you can  post questions we've also got the n8n templates  
14:20
library that's n8n.io/workflows really excited  for you to start your automation journey everyone  
14:26
at believes that you should own the means of your  automation and so on that note happy flowgramming