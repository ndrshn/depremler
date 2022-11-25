<template>
  <div
    class="os-input"
    :class="[
      size ? `os-input--${size}` : '',
      status ? `os-input--${status}` : '',
      {
        'os-input-group': $slots.prepend || $slots.append,
        'os-input--disabled': disabled,
        'os-input--prepend': $slots.prepend,
        'os-input--append': $slots.append,
      },
    ]"
  >
    <!-- S prepend element -->
    <div
      v-if="$slots.prepend"
      class="os-input-group__prepend"
      :class="{ 'os-input-group--button': prependButton }"
    >
      <slot name="prepend"></slot>
    </div>
    <!-- E prepend element -->

    <!-- S input -->
    <input
      class="os-input__original"
      :type="type"
      :name="name"
      :value="currentValue"
      :placeholder="placeholder"
      :min="min"
      :max="max"
      :minlength="minlength"
      :maxlength="maxlength"
      :disabled="disabled"
      :readonly="readonly"
      :autofocus="autofocus"
      @focus="handleFocus"
      @blur="handleBlur"
      @input="handleInput"
    />
    <!-- E input -->
    <!-- S append element -->
    <div
      v-if="$slots.append"
      class="os-input-group__append"
      :class="{ 'os-input-group--button': appendButton }"
    >
      <slot name="append"></slot>
    </div>
    <!-- E append element -->
  </div>
</template>

<script setup>
import { ref, watch, toRefs } from "vue";

const emit = defineEmits(["input", "focus", "change", "blur"]);
const props = defineProps({
  type: {
    type: String,
    default: "text",
  },
  value: [String, Number],
  name: String,
  placeholder: String,
  size: String,
  status: String,
  icon: String,
  prependButton: {
    type: Boolean,
    default: false,
  },
  appendButton: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  autofocus: {
    type: Boolean,
    default: false,
  },
  maxlength: Number,
  minlength: Number,
  max: Number,
  min: Number,
});

const { value: currentValue } = toRefs(props);

const handleFocus = (evt) => {
  emit("focus", evt);
};

const handleBlur = (evt) => {
  emit("blur", evt);
};

const handleInput = (evt) => {
  const value = evt.target.value;
  emit("input", value);
  emit("change", value);
};

const setCurrentValue = (val) => {
  if (val === currentValue.value) return;
  currentValue.value = val;
};

watch(
  () => props.value,
  (newVal) => {
    setCurrentValue(newVal);
  }
);
</script>

<style>
.os-input {
  position: relative;
  font-size: 0;
  line-height: 1.5;
  outline: 0;
  display: flex;
}

.os-input__original {
  display: block;
  width: 100%;
  padding: 6px 12px;
  color: #3f536e;
  font-size: 12px;
  background-color: #fff;
  border: 1px solid #c5d9e8;
  border-radius: 4px;
  -webkit-transition: border 0.2s;
  transition: border 0.2s;
  outline: none;
}

.os-input__original::-webkit-input-placeholder {
  color: #c9c9c9;
}

.os-input__original:-ms-input-placeholder {
  color: #c9c9c9;
}

.os-input__original::placeholder {
  color: #c9c9c9;
}

.os-input__original:hover {
  border-color: #79a1eb;
}

.os-input__original:focus {
  border-color: #79a1eb;
}

.os-input__icon {
  position: absolute;
  top: 0;
  right: 0;
  margin: 0 6px 0 0;
  width: 20px;
  height: 100%;
  color: #c5d9e8;
  font-size: 15px;
  text-align: center;
}

.os-input__icon:after {
  content: "";
  display: inline-block;
  width: 0;
  height: 100%;
  vertical-align: middle;
}

.os-input--disabled .os-input__original {
  color: #b1b1b1;
  background-color: #f7f7f7;
  border-color: #ececec;
  cursor: not-allowed;
}

.os-input--disabled .os-input__original::-webkit-input-placeholder {
  color: #c9c9c9;
}

.os-input--disabled .os-input__original:-ms-input-placeholder {
  color: #c9c9c9;
}

.os-input--disabled .os-input__original::placeholder {
  color: #c9c9c9;
}

.os-input--large {
  font-size: 14px;
}

.os-input--large .os-input__original {
  padding: 8px 14px;
}

.os-input--large .os-input__original::-webkit-input-placeholder {
  font-size: 14px;
}

.os-input--large .os-input__original:-ms-input-placeholder {
  font-size: 14px;
}

.os-input--large .os-input__original::placeholder {
  font-size: 14px;
}

.os-input--small {
  font-size: 11px;
}

.os-input--small .os-input__original {
  padding: 4px 10px;
}

.os-input--small .os-input__original::-webkit-input-placeholder {
  font-size: 11px;
}

.os-input--small .os-input__original:-ms-input-placeholder {
  font-size: 11px;
}

.os-input--small .os-input__original::placeholder {
  font-size: 11px;
}

.os-input--success .os-input__original {
  border-color: #13ce66;
}

.os-input--error .os-input__original {
  border-color: #ff4949;
}

.os-input--warning .os-input__original {
  border-color: #ffc82c;
}

.os-input--info .os-input__original {
  border-color: #78a4fa;
}

.os-input--prepend .os-input__original {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.os-input--append .os-input__original {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.os-input--icon .os-input__original {
  padding-right: 32px;
}

.os-input-group {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  line-height: normal;
  border-collapse: separate;
}

.os-input-group__prepend,
.os-input-group__append {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;
  padding: 0 10px;
  color: #9b9b9b;
  font-size: 12px;
  border: 1px solid #c5d9e8;
  border-radius: 4px;
  background-color: #f7f7f7;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  white-space: nowrap;
}

.os-input-group__prepend {
  border-right: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.os-input-group__append {
  border-left: 0;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.os-input-group--button {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-transition: backgroud 0.2s;
  transition: backgroud 0.2s;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  cursor: pointer;
}

.os-input-group--button:hover {
  background-color: #ececec;
}

.os-input-group--button:active {
  background-color: #dfdfdf;
}

.os-input-number {
  display: inline-block;
  position: relative;
  width: 100%;
  height: 32px;
  min-width: 80px;
  border: 1px solid #c5d9e8;
  border-radius: 4px;
  background-color: #fff;
  -webkit-transition: border 0.2s;
  transition: border 0.2s;
  overflow: hidden;
}

.os-input-number:hover:not(.os-input-number--disabled) {
  border-color: #79a1eb;
}

.os-input-number:hover:not(.os-input-number--disabled) .os-input-number__handler {
  opacity: 1;
}

.os-input-number__input {
  width: 100%;
  height: 100%;
}

.os-input-number__original {
  display: block;
  width: 100%;
  height: 100%;
  padding: 0 8px;
  color: #3f536e;
  line-height: 1.5;
  border: none;
  border-radius: 4px;
  background-color: #fff;
  outline: none;
}

.os-input-number input[type="number"] {
  -moz-appearance: textfield;
  background-color: transparent;
}

.os-input-number input[type="number"]::-webkit-inner-spin-button,
.os-input-number input[type="number"]::-webkit-outer-spin-button {
  margin: 0;
  -webkit-appearance: none;
}

.os-input-number__handler {
  position: absolute;
  top: 0;
  right: 0;
  width: 22px;
  height: 100%;
  border-left: 1px solid #dfdfdf;
  border-radius: 0 4px 4px 0;
  -webkit-transition: opacity 0.3s;
  transition: opacity 0.3s;
  opacity: 0;
}

.os-input-number__up,
.os-input-number__down {
  position: relative;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  width: 100%;
  height: 16px;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  color: #bfbfbf;
  font-size: 10px;
  text-align: center;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  cursor: pointer;
}

.os-input-number__up:hover:not(.os-input-number__up--disabled):not(.os-input-number__down--disabled),
.os-input-number__down:hover:not(.os-input-number__up--disabled):not(.os-input-number__down--disabled) {
  height: 18px;
  color: #9b9b9b;
}

.os-input-number__up:active:not(.os-input-number__up--disabled):not(.os-input-number__down--disabled),
.os-input-number__down:active:not(.os-input-number__up--disabled):not(.os-input-number__down--disabled) {
  background-color: #ececec;
}

.os-input-number__up--disabled,
.os-input-number__down--disabled {
  color: #ececec;
  cursor: not-allowed;
}

.os-input-number__down {
  border-top: 1px solid #dfdfdf;
}

.os-input-number__down:hover {
  margin-top: -2px;
}

.os-input-number--disabled {
  color: #b1b1b1;
  border-color: #ececec;
  background-color: #f7f7f7;
  cursor: not-allowed;
}

.os-input-number--disabled .os-input-number__original {
  color: #b1b1b1;
  cursor: not-allowed;
}

.os-input-number--disabled .os-input-number__handler {
  display: none;
}

.os-input-number--small {
  height: 28px;
}

.os-input-number--small .os-input-number__up,
.os-input-number--small .os-input-number__down {
  height: 14px;
  font-size: 9px;
}

.os-input-number--small .os-input-number__up:hover,
.os-input-number--small .os-input-number__down:hover {
  height: 16px !important;
}

.os-input-number--large {
  height: 36px;
}

.os-input-number--large .os-input-number__up,
.os-input-number--large .os-input-number__down {
  height: 18px;
  font-size: 11px;
}

.os-input-number--large .os-input-number__up:hover,
.os-input-number--large .os-input-number__down:hover {
  height: 20px !important;
}
</style>
