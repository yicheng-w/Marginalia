################################################################################
# Initializes the database for user login/storage                              #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#                                                                              #
# Description                                                                  #
#  Initializes database in db/ for user login and storage                      #
#                                                                              #
################################################################################

# TODO
#  create tables

# Dev Log
#  Project Created: 2015-12-19 12:42 - Yicheng W.

import sqlite3
from hashlib import sha256
from database import *

conn = sqlite3.connect("./db/infos.db")

c = conn.cursor()

create_base = "CREATE TABLE %s (%s)" # no user input needed, use %s

 # password = hexstring of hash
c.execute(create_base % ("users", "email TEXT, password TEXT, first TEXT, last TEXT"))

# note will be html source code with markup
c.execute(create_base % ("sites", "id INTEGER, email TEXT, title TEXT, site TEXT, comments TEXT, notes TEXT, shared INTEGER, t INTEGER"))

conn.commit()

m = sha256()
m.update("12345")
hash = m.hexdigest()

q = """INSERT INTO users VALUES (?, ?, ?, ?)"""

c.execute(q, ('alex.wyc2098@gmail.com', hash, 'Yicheng', 'Wang'))

conn.commit()

site = """
<h4>Does the Hate Crimes Bill Have 14th Amendment Problems?</h4>
<p>By ASHBY JONES</p>
<p>So, it looks like this hate crimes bill we&#8217;ve blogged on before (here and
here) is going to soon become law. The Senate on Thursday
voted 68-to-29 to approve the bill and thereby extend new federal protections to
people who are victims of violent crime because of their sex or sexual
orientation. The House approved the bill earlier this month. All it needs now is
a John Hancock from President Obama, who reportedly supports the bill. Click
here for the NYT story on the Senate vote. </p>

<p>The measure, named after Matthew Shepard (pictured), the gay University of
Wyoming student who was murdered in 1998, essentially broadens the definition of
federal hate crimes to include those committed because of a victim's gender or gender identity, or sexual orientation. It gives victims the same federal protections already given to people who are victims of violent crimes because of their race, color, religion or national origin.</p>
<p>A couple thoughts, before we leave this topic for the time being. The law got broad support from law-enforcement groups. But from where we sit, it&#8217;ll be interesting to see if the bill makes a real difference in combating crime.</p>
<p>The bill leaves the prosecution of hate crimes mostly in the hands of the states, 45 of which have their own hate-crimes legislation to begin with. The bill simply provides money to help state and local officials with the costs of prosecuting hate crimes and provides that the federal government can step in after the Justice Department certifies that a state does not have jurisdiction or is unable to carry out justice.</p>
<p>In a recent Washington Post &#8220;On Faith&#8221; column, College of
Charleston mathematics professor and founder of the Secular Coalition for
America, Herb Silverman eloquently articulates what we&#8217;ve written before
&#8212; that at best, the law could be merely symbolic and, at worst, the law
could lead to strange outcomes. </p>
<p>Writes Silverman: </p>
<blockquote><p>A crime is a crime, regardless of the victim&#8217;s race, color,
religion, national origin or sexual orientation. A murdered white heterosexual
male is no less dead than an Hispanic, gay Christian. Suppose three murders
occur: one for money, another out of jealousy, and a third because the victim is
a black, gay Wiccan. If the first two murderers are sentenced to 20 years in
prison and the third is sentenced to 30 years, would the families of the victims
in the first two cases feel they had received equal justice under the
law?</p></blockquote>
<p>It&#8217;ll also, we think, be interesting to see if on the grounds Silverman discusses, the law passes constitutional muster. Some have their doubts. </p>
<p>Nat Hentoff, writing in 
Real Clear Politics in August, focuses not on what might
appear to be the bill&#8217;s most obvious potential bugaboo &#8212; that it
runs afoul of the First Amendment &#8212; but that it might violate the
law&#8217;s 14th Amendment guarantee of equal protection. </p>
<p>Writes Hentoff: </p>
<blockquote><p>Leahy&#8217;s bill, like the counterpart &#8220;hate crimes&#8221; measure of House Judiciary Chairman John Conyers, D-Mich., that passed in the House this past April, violates the 14th Amendment&#8217;s equal protection under the laws for individual Americans by setting up a special collective class of victims whose assailants, when convicted, will be given extra punishment for crimes perceived to be based on gender identity, sexual orientation or disability, among other biases. Those who attack the elderly, police or those of the poor who are not among the &#8220;protected classes&#8221; would not get lengthier &#8220;hate&#8221; sentences than the law provides for the act itself. Doesn&#8217;t this make lesser citizens of their victims?</p></blockquote>
"""

title='Does the Hate Crimes Bill Have 14th Amendment Problems?'

add_to_sites("alex.wyc2098@gmail.com", title, site, '', "");
