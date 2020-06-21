# USER-API

## Texts
- Object identification (font etc.): `svg:text id=<name>`
  - Properties:
    - `style`
    e.g. 
    ```css
    font-style:normal;
    font-weight:normal;
    font-size:13.84628773px;
    line-height:1.25;
    font-family:sans-serif;
    letter-spacing:0px;
    word-spacing:0px;
    fill:#000000;
    fill-opacity:1;
    stroke:none;
    stroke-width:0.34615719;
    ```
    - normal CSS properties


- Object identification (text itself): `svg:tspan id=<name>`
- Properties:
  - none (content of text node is text itself)
  => parent `tspan` node has position
    - Properties:
      - `x`,`y` positions
	  - `style`
	    e.g. 
	    ```css
	    font-style:normal;
	    font-weight:normal;
	    font-size:13.84628773px;
	    line-height:1.25;
	    font-family:sans-serif;
	    letter-spacing:0px;
	    word-spacing:0px;
	    fill:#000000;
	    fill-opacity:1;
	    stroke:none;
	    stroke-width:0.34615719;
	    ```
	    - normal CSS properties

- Exposed Functionality:
  - Dynamic Size (CSS style settings and text box size)
  - Limit length (Backend functionality => setting in config file (e.g. `limit-length:17` for 17 chars)
  - Change Opacity
  - Changeable Colour (e.g. `style: fill:#1faf28` on parent node of text)
  - Fixed positioning (__High-level:__ Dynamic positioning)
    - seems like it would be nice to really parse the svg as a canvas
    - and be able to mirror items from a virtual middle line etc.
    - so to have basic geometric figures and really "know" where items are dependent to each other on this canvas
    - this would enable us to move text from one point to another in this "room" on the canvas


## Images
- Object identification: `svg:image id=<name>`
- dynamically embed images from an “assets” folder
- Change Opacity/Hide


## Groups
- Object identification: `svg:g id=<name>`
- Change Opacity/Hide


## Effects
- Connect different effects and order them into "pseudo-animations"

### Texts
### Images

## Animations
- Smooth Movement
- Blending in/out

## Data sources
- assign single values from data-sources to template variables
- DESIGN: deal with conditions ([Conditionals](#Conditionals))
- use a premade composition of free, open-source templates (rating, civ stats, etc.)

## Internationalization (i18n) & Localization (l10n)
- ability to change/set the languages output

## Conditionals
- model is event-based
- expose functionality by letting the user define the input and the implementation of the logic is our task
  - better understandability for users
  - e.g. `visibility_threshold_min: 1 / visibility_threshold_max: 999` instead of `hide-if: greater: 999`
  - set reasonable standard values
    - e.g. in the example up there `visibility_threshold_min: 1` should be set as a standardvalue
