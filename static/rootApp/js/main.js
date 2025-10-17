/**
 * Implementation of the accordion widget.
 * @author Andrey Glotov
 * @see {@link https://www.w3.org/TR/wai-aria-practices/#accordion}
 */

// ------------------------------ BEGIN CONSTANTS ------------------------------

const ClassNames = {
  ROOT: 'accordion',
  GROUP: 'accordion__group',
  PANEL_EXPANDED: 'accordion__panel_expanded' };


const Selectors = {
  TRIGGER: '.accordion__trigger',
  PANEL: '.accordion__panel' };


const Keys = {
  ENTER: 13,
  SPACE: 32,
  END: 35,
  HOME: 36,
  UP: 38,
  DOWN: 40 };


// ------------------------------- END CONSTANTS -------------------------------

// -------------------------- BEGIN UTILITY FUNCTIONS --------------------------

/**
 * Force a reflow
 * @param {HTMLElement} el The element whose styles have been changed
 */
function forceReflow(el) {
  void el.offsetHeight;
}

/**
   * Get transition duration for the specified element
   * @param {HTMLElement} el The element to compute transition duration on
   */
function getTransitionDuration(el) {
  const style = getComputedStyle(el);

  const duration = style.transitionDuration || '';
  const delay = style.transitionDelay || '';

  if (!duration && !delay) {
    return 0;
  }

  const floatDuration = parseFloat(duration.split(','));
  const floatDelay = parseFloat(delay.split(','));

  const msDuration = (floatDuration + floatDelay) * 1000;
  return isNaN(msDuration) ? 0 : msDuration;
}

/**
   * Detect the end of CSS transition.
   * @param {HTMLElement} el The element to detect transition end on
   */
function detectTransitionEnd(el) {
  const duration = getTransitionDuration(el);

  let handleTransitionEnd;

  return new Promise(resolve => {
    handleTransitionEnd = e => {
      if (e.target === el) {
        resolve();
      }
    };
    el.addEventListener('transitionend', handleTransitionEnd, false);

    // In case the 'transitionend' event is not supported, or is somehow lost,
    // or there is no transition property defined, setup a timer to resolve
    // the promise after the given duration
    setTimeout(resolve, duration);
  }).then(() => {
    el.removeEventListener('transitionend', handleTransitionEnd, false);
  });
}

// --------------------------- END UTILITY FUNCTIONS ---------------------------

/**
 * Accordion implementation
 */
class Accordion {
  /**
                  * Create an Accordion
                  * @param {HTMLElement} root The root node
                  * @param {Object} options The options object
                  * @param {boolean} options.allowToggle Allow for each header to both open and
                  *    close its panel. Makes it possible for all panels to be closed. Assumes
                  *    only one panel may be open.
                  * @param {boolean} options.allowMultiple Allow for multiple accordion panels
                  *    to be expanded at the same time. Assumes <tt>allowToggle</tt> is set to
                  *    <tt>true</tt>.
                  */
  constructor(root, options = {}) {
    const config = this._getConfig(options, root);

    const triggers = [],panels = [];
    let activeIndex = -1;

    [].forEach.call(root.children, (group, i) => {
      if (!group.classList.contains(ClassNames.GROUP)) {
        return;
      }

      const trigger = group.querySelector(Selectors.TRIGGER);
      const panel = group.querySelector(Selectors.PANEL);
      if (trigger == null || panel == null) {
        return;
      }

      triggers.push(trigger);
      panels.push(panel);

      let isExpanded = trigger.getAttribute('aria-expanded') === 'true';
      if (!config.allowMultiple && isExpanded) {
        if (activeIndex !== -1) {
          // Make sure that only one panel is expanded
          isExpanded = false;
        } else {
          activeIndex = i;
        }
      }

      // Make sure proper classes are applied
      if (isExpanded) {
        panel.classList.add(ClassNames.PANEL_EXPANDED);
      } else {
        panel.classList.remove(ClassNames.PANEL_EXPANDED);
      }
    });

    if (triggers.length === 0) {
      return;
    }

    if (!config.allowToggle && activeIndex === -1) {
      // Make sure at least one panel is expanded
      activeIndex = 0;
      triggers[0].setAttribute('aria-expanded', 'true');
      panels[0].classList.add(ClassNames.PANEL_EXPANDED);
    }

    this._elements = { root, triggers, panels };
    this._config = config;
    this._state = {
      activeIndex,
      isTransitioning: false };


    this._handleClick = this._handleClick.bind(this);
    this._handleKeyDown = this._handleKeyDown.bind(this);

    this.attachEvents();
  }

  // -------------------------- BEGIN PRIVATE METHODS --------------------------

  /**
   * Get configuration options from the provided object and <tt>data-*</tt>
   * attributes on the root element.
   * @param {object} options The configuration options
   * @return {object} an object containing configuration options
   */
  _getConfig(options, root) {
    const dataset = root.dataset;

    const allowToggle = !!options.allowToggle || dataset.allowToggle === 'true';
    const allowMultiple = allowToggle && (
    !!options.allowMultiple || dataset.allowMultiple === 'true');

    return {
      allowToggle,
      allowMultiple };

  }

  /**
     * Collapse the specified panel
     * @param {number} i The index of the panel to be collapsed
     * @return {Promise} A Promise which resolves when the transition is complete
     */
  _collapsePanel(i) {
    const trigger = this._elements.triggers[i];
    const panel = this._elements.panels[i];

    trigger.setAttribute('aria-expanded', 'false');

    const currentHeight = panel.getBoundingClientRect().height;
    panel.style.height = currentHeight + 'px';
    forceReflow(panel);

    panel.style.height = '0';

    return detectTransitionEnd(panel).then(() => {
      panel.style.height = '';
      panel.classList.remove(ClassNames.PANEL_EXPANDED);
    });
  }

  /**
     * Expand the specified panel
     * @param {number} i The index of the panel to be expanded
     * @return {Promise} A Promise which resolves when the transition is complete
     */
  _expandPanel(i) {
    const trigger = this._elements.triggers[i];
    const panel = this._elements.panels[i];

    trigger.setAttribute('aria-expanded', 'true');

    panel.classList.add(ClassNames.PANEL_EXPANDED);
    const targetHeight = panel.getBoundingClientRect().height;
    panel.style.height = '0';
    forceReflow(panel);

    panel.style.height = targetHeight + 'px';

    return detectTransitionEnd(panel).then(() => {
      panel.style.height = '';
    });;
  }

  // --------------------------- END PRIVATE METHODS ---------------------------

  // --------------------------- BEGIN EVENT HANDLERS --------------------------

  /**
   * Handle the click event for accordion headers
   * @param {MouseEvent} e The event to be handled
   * @param {number} i The index of the corresponding accordion group
   */
  _handleClick(e) {
    const trigger = e.target.closest(Selectors.TRIGGER);
    if (!trigger) {
      return;
    }

    const groupIndex = this._elements.triggers.indexOf(trigger);
    this.togglePanel(groupIndex);
  }

  /**
     * Handle the keydown event for accordion headers
     * @param {KeyboardEvent} e The event to be handled
     * @param {number} i The index of the corresponding accordion group
     */
  _handleKeyDown(e) {
    const { keyCode, target } = e;

    console.log(target);

    const trigger = target.closest(Selectors.TRIGGER);
    if (!trigger) {
      return;
    }

    const { triggers } = this._elements;
    const currentIndex = triggers.indexOf(trigger);

    if (keyCode == Keys.ENTER || keyCode == Keys.SPACE) {
      // Expand/collapse the associated panel
      this.togglePanel(currentIndex);

      e.preventDefault();
      e.stopPropagation();
    } else {
      const groupCount = triggers.length;
      let nextIndex;

      switch (e.keyCode) {
        case Keys.END:
          // Move focus to the last accordion header
          nextIndex = toggleCount - 1;
          break;

        case Keys.HOME:
          // Move focus to the first accordion header
          nextIndex = 0;
          break;

        case Keys.DOWN:
          // Moves focus to the next accordion header
          nextIndex = (groupCount + currentIndex + 1) % groupCount;
          break;

        case Keys.UP:
          // Move focus to the previous accordion header
          nextIndex = (groupCount + currentIndex - 1) % groupCount;
          break;}


      if (typeof nextIndex !== 'undefined') {
        this._elements.triggers[nextIndex].focus();
        e.preventDefault();
        e.stopPropagation();
      }
    }
  }

  // ---------------------------- END EVENT HANDLERS ---------------------------

  // --------------------------- BEGIN PUBLIC METHODS --------------------------

  /**
   * Toggle the specified panel
   * @param {number} The index of the panel to toggle
   */
  togglePanel(i) {
    if (i < 0 || i >= this._elements.panels.length) {
      return;
    }

    if (this._state.isTransitioning) {
      return;
    }

    if (!this._config.allowToggle && this._state.activeIndex === i) {
      // Configuration requires one panel to be expanded at all times
      return;
    }

    const trigger = this._elements.triggers[i];
    const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
    const isDisabled = trigger.getAttribute('aria-disabled') === 'true';

    if (isExpanded && isDisabled) {
      // The panel isn't permitted to be collapsed
      return;
    }

    this._state.isTransitioning = true;

    if (this._config.allowToggle) {
      if (isExpanded) {
        this._collapsePanel(i).then(() => {
          if (!this._config.allowMultiple) {
            this._state.activeIndex = -1;
          }
          this._state.isTransitioning = false;
        });
      } else {
        this._expandPanel(i).then(() => {
          if (!this._config.allowMultiple) {
            this._state.activeIndex = i;
          }
          this._state.isTransitioning = false;
        });
      }
    } else {
      Promise.all([
      this._collapsePanel(this._state.activeIndex),
      this._expandPanel(i)]).
      then(() => {
        this._state.activeIndex = i;
        this._state.isTransitioning = false;
      });
    }
  }

  /**
     * Attach all event listeners
     */
  attachEvents() {
    const { root } = this._elements;

    root.addEventListener('click', this._handleClick, false);
    root.addEventListener('keydown', this._handleKeyDown, false);
  }

  /**
     * Detach all event listeners
     */
  detachEvents() {
    const { root } = this._elements;

    root.removeEventListener('click', this._handleClick, false);
    root.removeEventListener('keydown', this._handleKeyDown, false);
  }

  /**
     * Initialize all accordion blocks on the page.
     */
  static initAll() {
    [].forEach.call(document.getElementsByClassName(ClassNames.ROOT), el => {
      new Accordion(el);
    });
  }

  // ---------------------------- END PUBLIC METHODS ---------------------------
}

Accordion.initAll();

 // $('#resultBox').css("display","none");

$("#searchbtn").click(function () {

    // Set the effect type
    var effect = 'slide';

    // Set the options for the effect type chosen
    var options = { direction: "left" };

    // Set the duration (default: 400 milliseconds)
    var duration = 15000;

    $('#resultBox').css("display","block");
    $('#resultBox').toggle(effect, options, duration);
});


$("#close").click(function () {
  $('#resultBox').css("display","none");
});
