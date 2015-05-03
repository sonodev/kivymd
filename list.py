# -*- coding: utf-8 -*-
import material_resources as m_res
from layouts import MaterialGridLayout, MaterialRelativeLayout, \
	MaterialBoxLayout
from label import MaterialLabel
from divider import Divider
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.metrics import dp, sp
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior


class List(MaterialRelativeLayout):

	def __init__(self, **kwargs):
		super(List, self).__init__(**kwargs)
		self.sv = ScrollView(do_scroll_x=False)
		self.gl = MaterialGridLayout(cols=1,
		                             padding=(0, m_res.LIST_VERTICAL_PADDING,
		                                      0, m_res.LIST_VERTICAL_PADDING),
		                             height=2 * m_res.LIST_VERTICAL_PADDING,
		                             size_hint_y=None)
		self.sv.add_widget(self.gl)
		self.add_widget(self.sv)

	def add_widget(self, widget, index=0):
		if isinstance(widget, _ListItem):
			self.gl.add_widget(widget)
			self.gl.height += widget.height
		else:
			super(List, self).add_widget(widget, index)

	def clear(self):
		self.gl.height = 2 * m_res.LIST_VERTICAL_PADDING
		self.gl.clear_widgets()


class _ListItem(ButtonBehavior, MaterialRelativeLayout):
	text_top_padding = NumericProperty(0)
	text_bottom_padding = NumericProperty(0)
	text = StringProperty()
	divider = BooleanProperty(True)

	def __init__(self, **kwargs):
		self.size_hint_y = None
		self.bl_text = MaterialBoxLayout(
			orientation="vertical",
			size_hint_y=None,
			x=dp(16),
			padding=[0, self.text_top_padding,
			         m_res.HORIZ_MARGINS, self.text_bottom_padding])
		self.bind(height=self.bl_text.setter('height'))
		self.lbl_primary = MaterialLabel(color=m_res.TEXT_COLOR,
		                                 font_size=sp(16))
		self._divider = Divider()
		self.bl_text.bind(x=self._divider.setter('x'),
		                  width=self._divider.setter('width'))
		super(_ListItem, self).__init__(**kwargs)
		self.bl_text.add_widget(self.lbl_primary)
		self.add_widget(self.bl_text)

		self.add_widget(self._divider)

	def on_width(self, instance, value):
		self.bl_text.width = self.width - self.bl_text.x

	def on_text(self, instance, value):
		self.lbl_primary.text = value

	def on_divider(self, instance, value):
		if value:
			self._divider.opacity = 100
		else:
			self._divider.opacity = 0


class _ListItemWithImage(_ListItem):
	image = StringProperty(m_res.ICON_DEFAULT)
	_image_size = (dp(0), dp(0))

	def __init__(self, **kwargs):
		self._image = Image(x=dp(16),
		                    size_hint=(None, None),
		                    size=self._image_size,
		                    source=self.image)
		super(_ListItemWithImage, self).__init__(**kwargs)
		self.bl_text.x = dp(72)
		self.add_widget(self._image)

	def on_height(self, instance, value):
		self._image.y = self.bl_text.height/2 - self._image.height/2

	def on_image(self, instance, value):
		self._image.source = value


class SingleLineItem(_ListItem):
	text_top_padding = dp(16)
	text_bottom_padding = dp(20)

	def __init__(self, **kwargs):
		super(SingleLineItem, self).__init__(**kwargs)
		self.height = dp(48)


class SingleLineItemWithIcon(SingleLineItem, _ListItemWithImage):
	_image_size = (dp(24), dp(24))

	def __init__(self, **kwargs):
		super(SingleLineItemWithIcon, self).__init__(**kwargs)


class SingleLineItemWithAvatar(SingleLineItemWithIcon, _ListItemWithImage):
	height = dp(56)
	text_top_padding = dp(20)
	text_bottom_padding = dp(24)
	_image_size = (dp(48), dp(48))


class TwoLineItem(_ListItem):
	secondary_text = StringProperty()

	def __init__(self, **kwargs):
		self.text_top_padding = dp(20)
		self.text_bottom_padding = dp(20)
		self.lbl_secondary = MaterialLabel(color=m_res.SECONDARY_TEXT_COLOR,
		                                   font_size=sp(14))
		super(TwoLineItem, self).__init__(**kwargs)
		self.height = dp(72)
		self.bl_text.spacing = dp(8)
		self.bl_text.add_widget(self.lbl_secondary)

	def on_secondary_text(self, instance, value):
		self.lbl_secondary.text = value


class TwoLineItemWithIcon(TwoLineItem, _ListItemWithImage):
	_image_size = (dp(24), dp(24))


class TwoLineItemWithAvatar(TwoLineItemWithIcon, _ListItemWithImage):
	_image_size = (dp(48), dp(48))

	def __init__(self, **kwargs):
		super(TwoLineItemWithAvatar, self).__init__(**kwargs)


class ThreeLineItem(_ListItem):
	height = dp(88)


class ThreeLineItemWithAvatar(ThreeLineItem, _ListItemWithImage):

	def on_height(self, instance, value):
		self._image.y = self.bl_text.height - self.text_top_padding - \
		                self._image.height