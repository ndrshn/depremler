<template>
  <button
    class="os-btn"
    :class="[
      props.type ? `os-btn--${props.type}` : '',
      props.size ? `os-btn--${props.size}` : '',
      parent && parent.size ? `os-btn--${parent.size}` : '',
      props.hollow ? `os-btn--${props.type}--hollow` : '',
      props.circle && !slots.default ? 'os-btn--circle' : '',
    ]"
    :style="styleList"
    :disabled="props.disabled"
    :type="nativeType"
    @click="handleClick"
  >
    <i v-if="props.loading" class="os-btn__loading icon icon-loader"></i>
    <i v-if="props.icon" class="os-btn__icon ti" :class="`ti-${props.icon}`"></i>
    <span v-if="slots.default" class="os-btn__text">
      <slot></slot>
    </span>
  </button>
</template>

<script setup>
import { getCurrentInstance, computed, useSlots } from "vue";

const instance = getCurrentInstance();
const parent = instance.parent;
const slots = useSlots();
const emit = defineEmits(["click"]);
const props = defineProps({
  type: {
    type: String,
    default: "default",
  },
  nativeType: {
    type: String,
    default: "button",
  },
  size: {
    type: String,
    default: "normal",
  },
  icon: {
    type: String,
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  hollow: {
    type: Boolean,
    default: false,
  },
  circle: {
    type: Boolean,
    default: false,
  },
});

const styleList = computed(() => {
  let userStyle = {};

  if (props.style) {
    userStyle = props.style;
  }

  return Object.assign(userStyle, {
    marginRight: `${parent.gap}px`,
  });
});

const handleClick = (evt) => {
  if (props.loading || props.disabled) {
    evt.preventDefault();
    return;
  }
  emit("click", evt);
};
</script>

<style>
.os-btn {
  display: inline-block;
  padding: 6px 16px;
  font-size: 0;
  outline: 0;
  line-height: 1.5;
  text-align: center;
  white-space: nowrap;
  border: 1px solid #c5d9e8;
  border-radius: 4px;
  background-color: #fff;
  -webkit-transition: background 0.2s;
  transition: background 0.2s;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  cursor: pointer;
}

.os-btn:hover {
  background-color: #ecf5ff;
}

.os-btn:active {
  background-color: #e2ecf4;
}

.os-btn:disabled,
.os-btn:disabled:hover,
.os-btn:disabled:active {
  cursor: not-allowed;
  color: #d2d2d2;
  border-color: #ececec;
  background-color: #f7f7f7;
}

.os-btn--primary,
.os-btn--success,
.os-btn--error,
.os-btn--warning,
.os-btn--info {
  color: #fff;
}

.os-btn--default--hollow {
  background: none;
  color: #3f536e;
}

.os-btn--default--hollow:hover {
  background: none;
  color: #5c6d84;
  border-color: #cedfeb;
}

.os-btn--default--hollow:active {
  background: none;
  color: #52647d;
  border-color: #cbddea;
}

.os-btn--primary {
  border-color: #6190e8;
  background-color: #6190e8;
}

.os-btn--primary:hover {
  background-color: #79a1eb;
  border-color: #79a1eb;
}

.os-btn--primary:active {
  background-color: #5782d1;
  border-color: #5782d1;
}

.os-btn--primary--hollow {
  background: none;
  color: #6190e8;
}

.os-btn--primary--hollow:hover {
  background: none;
  color: #79a1eb;
  border-color: #79a1eb;
}

.os-btn--primary--hollow:active {
  background: none;
  color: #719bea;
  border-color: #719bea;
}

.os-btn--success {
  border-color: #13ce66;
  background-color: #13ce66;
}

.os-btn--success:hover {
  background-color: #36d57d;
  border-color: #36d57d;
}

.os-btn--success:active {
  background-color: #11b95c;
  border-color: #11b95c;
}

.os-btn--success--hollow {
  background: none;
  color: #13ce66;
}

.os-btn--success--hollow:hover {
  background: none;
  color: #36d57d;
  border-color: #36d57d;
}

.os-btn--success--hollow:active {
  background: none;
  color: #2bd375;
  border-color: #2bd375;
}

.os-btn--error {
  border-color: #ff4949;
  background-color: #ff4949;
}

.os-btn--error:hover {
  background-color: #ff6464;
  border-color: #ff6464;
}

.os-btn--error:active {
  background-color: #e64242;
  border-color: #e64242;
}

.os-btn--error--hollow {
  background: none;
  color: #ff4949;
}

.os-btn--error--hollow:hover {
  background: none;
  color: #ff6464;
  border-color: #ff6464;
}

.os-btn--error--hollow:active {
  background: none;
  color: #ff5b5b;
  border-color: #ff5b5b;
}

.os-btn--warning {
  border-color: #ffc82c;
  background-color: #ffc82c;
}

.os-btn--warning:hover {
  background-color: #ffd04c;
  border-color: #ffd04c;
}

.os-btn--warning:active {
  background-color: #e6b428;
  border-color: #e6b428;
}

.os-btn--warning--hollow {
  background: none;
  color: #ffc82c;
}

.os-btn--warning--hollow:hover {
  background: none;
  color: #ffd04c;
  border-color: #ffd04c;
}

.os-btn--warning--hollow:active {
  background: none;
  color: #ffce41;
  border-color: #ffce41;
}

.os-btn--info {
  border-color: #78a4fa;
  background-color: #78a4fa;
}

.os-btn--info:hover {
  background-color: #8cb2fb;
  border-color: #8cb2fb;
}

.os-btn--info:active {
  background-color: #6c94e1;
  border-color: #6c94e1;
}

.os-btn--info--hollow {
  background: none;
  color: #78a4fa;
}

.os-btn--info--hollow:hover {
  background: none;
  color: #8cb2fb;
  border-color: #8cb2fb;
}

.os-btn--info--hollow:active {
  background: none;
  color: #86adfb;
  border-color: #86adfb;
}

.os-btn--link {
  background: none !important;
  color: #6190e8;
  border: none !important;
}

.os-btn--link:hover {
  background: none !important;
  color: #8cb2fb;
  border-color: #ffffff26;
}

.os-btn--link:active {
  background: none !important;
  color: #8cb2fb;
  border-color: #ffffff1a;
}

.os-btn--link:disabled,
.os-btn--link:disabled:hover,
.os-btn--link:disabled:active {
  background: none;
}

.os-btn--text {
  background: none;
  color: #3f536e;
  border: none !important;
}

.os-btn--text:hover {
  background-color: #ecf5ff;
  color: #719bea;
  border-color: #ffffff26;
}

.os-btn--text:active {
  background-color: #ecf5ff;
  color: #719bea;
  border-color: #ffffff1a;
}

.os-btn--text:disabled,
.os-btn--text:disabled:hover,
.os-btn--text:disabled:active {
  background: none;
}

.os-btn--default--hollow:disabled,
.os-btn--default--hollow:disabled:hover,
.os-btn--default--hollow:disabled:active,
.os-btn--primary--hollow:disabled,
.os-btn--primary--hollow:disabled:hover,
.os-btn--primary--hollow:disabled:active,
.os-btn--success--hollow:disabled,
.os-btn--success--hollow:disabled:hover,
.os-btn--success--hollow:disabled:active,
.os-btn--error--hollow:disabled,
.os-btn--error--hollow:disabled:hover,
.os-btn--error--hollow:disabled:active,
.os-btn--warning--hollow:disabled,
.os-btn--warning--hollow:disabled:hover,
.os-btn--warning--hollow:disabled:active,
.os-btn--info--hollow:disabled,
.os-btn--info--hollow:disabled:hover,
.os-btn--info--hollow:disabled:active,
.os-btn--link--hollow:disabled,
.os-btn--link--hollow:disabled:hover,
.os-btn--link--hollow:disabled:active,
.os-btn--text--hollow:disabled,
.os-btn--text--hollow:disabled:hover,
.os-btn--text--hollow:disabled:active {
  background: none;
}

.os-btn--large {
  font-size: 14px;
  padding: 8px 16px;
}

.os-btn--large.os-btn--circle {
  width: 40px;
  height: 40px;
}

.os-btn--large.os-btn--circle .os-btn__icon {
  font-size: 16px;
}

.os-btn--large .os-btn__text {
  font-size: 14px;
}

.os-btn--small {
  font-size: 11px;
  padding: 4px 12px;
}

.os-btn--small.os-btn--circle {
  width: 28px;
  height: 28px;
}

.os-btn--small.os-btn--circle .os-btn__icon,
.os-btn--small .os-btn__text {
  font-size: 11px;
}

.os-btn--smaller {
  font-size: 10px;
  padding: 2px 10px;
}

.os-btn--smaller.os-btn--circle {
  width: 24px;
  height: 24px;
}

.os-btn--smaller.os-btn--circle .os-btn__icon,
.os-btn--smaller .os-btn__text {
  font-size: 10px;
}

.os-btn--circle {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 50%;
}

.os-btn--circle .os-btn__icon {
  font-size: 14px;
}

.os-btn__icon,
.os-btn__loading {
  font-size: 12px;
  line-height: 1.5;
}

.os-btn__icon + span,
.os-btn__loading + span {
  margin-left: 4px;
}

.os-btn__loading {
  display: inline-block;
  line-height: 1;
  -webkit-animation: loadingCircle 1s linear infinite;
  animation: loadingCircle 1s linear infinite;
}

.os-btn__text {
  font-size: 12px;
}

@-webkit-keyframes loadingCircle {
  0% {
    -webkit-transform: rotate(0);
    transform: rotate(0);
  }

  to {
    -webkit-transform: rotate(1turn);
    transform: rotate(1turn);
  }
}

@keyframes loadingCircle {
  0% {
    -webkit-transform: rotate(0);
    transform: rotate(0);
  }

  to {
    -webkit-transform: rotate(1turn);
    transform: rotate(1turn);
  }
}
</style>
