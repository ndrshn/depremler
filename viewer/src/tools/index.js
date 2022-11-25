const SPECIAL_CHARS_REGEXP = /([:\-_]+(.))/g
const MOZ_HACK_REGEXP = /^moz([A-Z])/

export function camelCase(name) {
  return name.replace(SPECIAL_CHARS_REGEXP, function (_, separator, letter, offset) {
    return offset ? letter.toUpperCase() : letter
  }).replace(MOZ_HACK_REGEXP, 'Moz$1')
}

function typeOf(obj) {
  const map = {
    '[object Boolean]': 'boolean',
    '[object Number]': 'number',
    '[object String]': 'string',
    '[object Function]': 'function',
    '[object Array]': 'array',
    '[object Date]': 'date',
    '[object RegExp]': 'regExp',
    '[object Undefined]': 'undefined',
    '[object Null]': 'null',
    '[object Object]': 'object',
  }
  return map[Object.prototype.toString.call(obj)]
}

export function deepCopy(data) {
  const type = typeOf(data)
  let obj

  if (type === 'array') {
    obj = []
  } else if (type === 'object') {
    obj = {}
  } else {
    return data
  }

  if (type === 'array') {
    for (let i = 0; i < data.length; i++) {
      obj.push(deepCopy(data[i]))
    }
  } else if (type === 'object') {
    for (const i in data) {
      obj[i] = deepCopy(data[i])
    }
  }

  return obj
}

export function findComponentsDownward(context, componentName, components = []) {
  const childrens = context.vnode.children
  console.log(context)
  if (childrens && childrens.length) {
    childrens.forEach(child => {
      const subChildren = child.children
      const name = child.localName;
      if (name === componentName) {
        components.push(child)
      }
      if (subChildren.length) {
        const findChildren = findComponentsDownward(child, componentName, components)
        if (findChildren) {
          components.concat(findChildren)
        }
      }
    })
  }
  return components
}