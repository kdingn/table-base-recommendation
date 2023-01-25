<template>
  <div>
    <b-container>
      <b-row>
        <b-col v-for="n in 8" :key=n>
          <b-img src="https://picsum.photos/200/200" class="m-3" id="popover-target" thumbnail/>
          <b-popover target="popover-target" triggers="hover" placement="top">
            <template #title>Popover Title{{n}}</template>
            I am popover <b>component</b> content!
          </b-popover>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>