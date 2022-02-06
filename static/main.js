var app = new Vue({
  el: "#app",
  data() {
    return {
      items: [],
      filterParams: {},
    }
  },
  methods: {
    getItems: function (event) {
      const params = new URLSearchParams(this.filterParams);
      axios
        .get('http://localhost:8000/api/v1/levels', {params})
        .then(response => (this.items = response.data.results)).catch(error => {
        console.log(error);
        this.errored = true;
      });
    },
    setUser: function (event) {
      this.filterParams.user_id = event.target.value;
      this.getItems()
    },
    setTimeStart: function (event) {
      this.filterParams.start = event.target.value;
      this.getItems()
    },
    setTimeStop: function (event) {
      this.filterParams.stop = event.target.value;
      this.getItems()
    },
    setOrdering: function (event, param) {
      console.log(param);
      if (this.filterParams.ordering === param) {
        this.filterParams.ordering = "-" + param;
      } else {
        this.filterParams.ordering = param;
      }
      this.getItems()
    },
    setPageSize: function (event) {
      this.filterParams.page_size = event.target.value;
      this.getItems()
    },
    setPageNum: function (event) {
      this.filterParams.page = event.target.value;
      this.getItems()
    },
  }

})