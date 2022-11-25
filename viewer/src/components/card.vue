<template>
  <div
    class="os-card"
    :class="{
      'os-card--bordered': props.bordered,
      'os-card--no-hover': props.noHover,
    }"
  >
    <div class="os-card__head" v-if="props.title || !(!slots.title && !slots.extra)">
      <div class="os-card__title" v-if="props.title || slots.title">
        <span v-if="props.title">{{ props.title }}</span>
        <slot v-else name="title"></slot>
      </div>
      <div class="os-card__extra" v-if="slots.extra">
        <slot name="extra"></slot>
      </div>
    </div>
    <div class="os-card__body" :style="props.bodyStyle">
      <slot v-if="!props.loading"></slot>
      <slot v-else name="loading">
        <div class="os-card__body--loading">
          <div>
            <span style="width: 95%"></span>
          </div>
          <div>
            <span style="width: 32%"></span>
            <span style="width: 58%"></span>
          </div>
          <div>
            <span style="width: 23%"></span>
            <span style="width: 65%"></span>
          </div>
          <div>
            <span style="width: 59%"></span>
            <span style="width: 32%"></span>
          </div>
          <div>
            <span style="width: 26%"></span>
            <span style="width: 10%"></span>
            <span style="width: 50%"></span>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { useSlots } from "vue";

const slots = useSlots();

const props = defineProps({
  title: {
    type: String,
  },
  bordered: {
    type: Boolean,
    default: true,
  },
  noHover: {
    type: Boolean,
    default: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  bodyStyle: {
    type: Object,
  },
});
</script>

<style>
.os-card {
  position: relative;
  border-radius: 4px;
  background-color: #fff;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
}

.os-card:not(.os-card--no-hover):hover {
  border-color: #f7f7f7;
  -webkit-box-shadow: 1px 0 16px 0 rgba(100, 100, 100, 0.2);
  box-shadow: 1px 0 16px #64646433;
}

.os-card__head {
  padding: 0 12px;
  height: 36px;
  line-height: 36px;
  border-bottom: 1px solid #ececec;
}

.os-card__title {
  display: inline-block;
}

.os-card__extra {
  float: right;
}

.os-card__body {
  padding: 12px;
}

.os-card__body--loading span {
  display: inline-block;
  margin: 5px 1%;
  height: 14px;
  border-radius: 2px;
  background: -webkit-gradient(
    linear,
    left top,
    right top,
    from(rgba(192, 198, 206, 0.12)),
    color-stop(rgba(192, 198, 206, 0.2)),
    to(rgba(192, 198, 206, 0.12))
  );
  background: linear-gradient(
    90deg,
    rgba(192, 198, 206, 0.12),
    rgba(192, 198, 206, 0.2),
    rgba(192, 198, 206, 0.12)
  );
  background-size: 600% 600%;
  -webkit-animation: card-loading 1.4s ease infinite;
  animation: card-loading 1.4s ease infinite;
}

.os-card--bordered {
  border: 1px solid #ececec;
}

@-webkit-keyframes card-loading {
  0%,
  to {
    background-position: 0 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

@keyframes card-loading {
  0%,
  to {
    background-position: 0 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}
</style>
