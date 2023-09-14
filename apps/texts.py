
checkpage_messages = {0: 'Artist matches have not been saved',
                      1: 'Album matches have not been saved',
                      2: 'Unlinked albums have not been saved'}
wf_cmpart = """\
Intended workflow:


Select an artist in the left-hand side column and use the `Check Artist` button to see if it's present on the right-hand side.

If it is, a relation between the two will be established. You can tell by the number appearing in the Match column.
If it isn't, the `Add Artist` dialog will pop up with the artist name shown in the `last name` field.

To add the artist to the collection, complete the entries and press `Save`. After confirmation, this will make the name appear in the list on the right-hand side and establish the relation (again, indicated in the Match column).

To save the entire list to the Albums database, press `Save All`. The relations will also be saved, they are needed to keep track of artists " that have already been matched.
"""
wf_cmpalb = """\
Intended workflow:


Select an artist in the combobox at the top and see two lists of al" bums appear: albums present in the Clementine and Albums databases respectively. You can tell if a relation exists by the value in " the second column (an X or a number indicating the right-hand side " album's id).

Select an album in the left-hand side list and press the `Check Album` button to match it with one of the albums on the right-hand " side. A selection dialog will pop up where you can choose an album "
from the right-hand side to esablish a relation with.

If no right-hand side albums are available or you cancel the `Select Album` dialog because none is the right one, a dialog will open with " the `title` field set to the left-hand side's album title so you can " add a new one and make a relation with it.

To save the entire list to the Albums database, press `Save All`. Newly created albums will be saved to the Albums database together with their " tracks. The relations will also be saved, they are needed to keep track " of albums that have already been matched.

For now, you have to save the added/changed albums and relations before you proceed to another artist or change panels.
"""
wf_cmptrk = """\
Intended workflow:


Select an artist and an album in the two comboboxes at the top and if two lists of tracks appear, that means that most of the work" has been done.

It's possible, however, that the wrong album has been matched or that the tracks have not been imported into the Albums database.

This panel is intended to do a final comparison and correct eventual errors.
"""
workflows = {'cmpart': wf_cmpart, 'cmpalb': wf_cmpalb, 'cmptrk': wf_cmptrk}
