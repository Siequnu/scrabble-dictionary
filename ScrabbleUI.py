# Gist export 0.91

import ui
import sowpodsDictionaryList
import twl
import sound
		
def updateLabel (result, sender):
	if result == '1':
		changeButtonColor ('#023d02', sender)
		changeButtonImage ('checkmark', sender)
		changeButtonTintColor ('#ffffff', sender)
		sound.play_effect('game:Ding_3')
	elif result == '0':
		changeButtonColor ('#a0a0a0', sender)
		changeButtonImage ('wrong', sender)
		changeButtonTintColor ('#ffffff', sender)
		sound.play_effect('game:Error')
	
def changeButtonTintColor (hex, sender):
	button = sender.superview['button1']
	button.tint_color = hex
			
def changeButtonColor (hex, sender):
	button = sender.superview['button1']
	button.bg_color = hex


def changeButtonImage (image, sender):
	button = sender.superview['button1']
	checkmark = ui.Image.named('iob:checkmark_256')
	wrong = ui.Image.named('iob:close_256')
	search = ui.Image.named('iob:ios7_search_256')
	
	if image == 'checkmark':
		button.image = checkmark
	elif image == 'wrong':
		button.image = wrong
	elif image == 'search':
		button.image = search
		
				
def offlineSearch (word, dictionary):
	if dictionary == 0:
		dictionary = sowpodsDictionaryList.sowpodsDictionary
		if word.upper() in dictionary:
			return '1'
		else:
			return '0'
	elif dictionary == 1:
		if twl.check(word.lower()) == True:
			return '1'
		else:
			return '0'
	
	
def searchWord(sender):
	
	# Get word from entry field
	word = sender.superview['textfield1'].text
	
	# Set the selected dictionary as index
	activeDictionary = sender.superview['segmentedcontrol2'].selected_index
	
	# Get word validation from selected dictionary
	if activeDictionary == 0:
		# Offline
		wordIsValid = offlineSearch(word, activeDictionary)
	elif activeDictionary == 1:
		# Offline
		wordIsValid = offlineSearch(word, activeDictionary)
		
	# Update UI with results
	updateLabel (wordIsValid, sender)
	
# Segmented control logic
def button_action(sender):
	# If no word is in the box then don't trigger
	boxContents = sender.superview['textfield1'].text
	if boxContents:
		searchWord(sender)
	else:	
		# If no word then clean up label
		changeButtonColor ('f6f6f6', sender)
		changeButtonTintColor('#034c03', sender)
		changeButtonImage('search', sender)

								
# Create the UI and view
view = ui.View()
view.name = 'Scrabble Dictionary'
view.background_color = '#f6f6f6'
deviceScreenSizeX, deviceScreenSizeY = ui.get_screen_size()
view.height = deviceScreenSizeY
view.width = deviceScreenSizeX

# Draw the UI 
height = view.height
width = view.width

# Textfield
# Delegate class to handle textbox input events
class TextFieldDelegate (object):
	def textfield_did_change(sender):
		search = ui.Image.named('iob:ios7_search_256')
		sender.superview['button1'].image = search
		sender.superview['button1'].bg_color = '#f6f6f6'
		sender.superview['button1'].tint_color = '#034c03'

searchBar = ui.TextField(name = 'textfield1', placeholder = 'Enter a word...')
searchBar.font = ('<system>', 27)
searchBar.width = (width - (width/15)) # When centered, this will leave a small gap at either side
searchBar.height = 85
searchBar.center = (width/2, height/7)
searchBar.flex = 'R' # Check this value
searchBar.alignment = ui.ALIGN_CENTER
searchBar.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
searchBar.autocorrection_type = 'None'
searchBar.spellchecking_type = 'None'
searchBar.action = button_action
searchBar.clear_button_mode = 'always'
searchBar.delegate = TextFieldDelegate
view.add_subview(searchBar)

# Search Button
searchButton = ui.Button (name = 'button1', action = button_action)
searchButton.height = 85
searchButton.width = 85
searchButton.corner_radius = 6
searchButton.center = (width/2, height/7*2)
searchIcon = ui.Image.named('iob:ios7_search_256')
searchButton.image = searchIcon
searchButton.bg_color = '#f6f6f6'
searchButton.tint_color = '#034c03'
view.add_subview(searchButton)

# Segmented controller
dictionaryController = ui.SegmentedControl (name = 'segmentedcontrol2')
dictionaryController.action = button_action
dictionaryController.segments = ['SOWPODS', 'TWL06']
dictionaryController.selected_index = 0 
dictionaryController.bg_color = '#ffffff'
dictionaryController.tint_color = '#034c03'
dictionaryController.corner_radius = 5
dictionaryController.width = (width - (width/15))
dictionaryController.center = (width/2, height/7*3)
view.add_subview(dictionaryController)

# Definition button

# Present view
view.present(hide_title_bar = False, animated = False, style= 'full_screen')

