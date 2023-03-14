
function getSelector(elm)
{
if (elm.tagName === "BODY") return "BODY";
const names = [];
while (elm.parentElement && elm.tagName !== "BODY") {
    if (elm.id) {
        names.unshift("#" + elm.getAttribute("id")); // getAttribute, because elm.id could also return a child element with name "id"
        break; // Because ID should be unique, no more is needed. Remove the break, if you always want a full path.
    } else {
        let c = 1, e = elm;
        for (; e.previousElementSibling; e = e.previousElementSibling, c++) ;
        names.unshift(elm.tagName + ":nth-child(" + c + ")");
    }
    elm = elm.parentElement;
}
return names.join(">");
}

function add_to_cart(food_name) {
let element = document.querySelector(getSelector([...document.querySelectorAll('span')].filter(x => x.innerText.includes(food_name))[0]).split('>').slice(0, -4).join('>')+'>div:nth-child(3)>div:nth-child(1)>button')
element.click()
}

function get_element(name, type) {
    var aTags = document.getElementsByTagName(type);
    var searchText = name;
    var found;

    for (var i = 0; i < aTags.length; i++) {
    if (aTags[i].textContent == searchText) {
        found = aTags[i];
        break;
    }
    return found;
}
}

function push(text, type) {
    let element = get_element(text, type);
    element.click();
}

function send_form(input_text, form_text, type) {
    let selector = getSelector([...document.querySelectorAll(type)].filter(x => x.innerText.includes(form_text))[0])
    input = document.querySelector(selector);
    input.value = input_text;
    input.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keypress', { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
}

function check_all_in_document( )
{
  var c = new Array();
  c = document.getElementsByTagName('input');
  for (var i = 0; i < c.length; i++)
  {
    if (c[i].type == 'checkbox')
    {
      c[i].checked = true;
    }
  }
}