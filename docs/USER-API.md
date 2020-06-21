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
  - Changeable Colour (e.g. `style: fill:#1faf28` on parent node of text)
  - Fixed/Dynamic positioning
    - 



## Images
- Object identification: `svg:image id=<name>`
- dynamically embed images from an “assets” folder


## Groups
- Object identification: `svg:g id=<name>`




• Effects on Texts and Images
- Smooth Movement
- Blending in/out
- Change Opacity

• Animations
- Connect different effects and order them into animations

• Data sources
- assign single values from data-sources to template variables
- use a premade composition of free, open-source templates (rating, civ stats, etc.)

• Internationalization (i18n) & Localization (l10n)
- ability to change/set the languages output
