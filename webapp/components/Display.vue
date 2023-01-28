<template>
  <div>
    <b-container>
      <b-row>
        <b-col v-for="el in df">
          <a :href="el.url">{{el.id}}{{el.item}}</a>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";

var defaultPage = 1
var defaultContentsToShow = ""
var defaultContentsIn1Page = 100

export default {
  data() {
    return {
      page: defaultPage,
      contentsToShow: defaultContentsToShow,
      contentsIn1Page: defaultContentsIn1Page,
			df: [],
    }
  },
  mounted() {
    var url = new URL("http://localhost:5000/datas")
    url.searchParams.append("page", this.page)
    url.searchParams.append("contentsToShow", this.contentsToShow)
    url.searchParams.append("contentsIn1Page", this.contentsIn1Page)
    axios
      .get(url)
      .then((response) => (this.df = response.data))
  },
}
</script>