<template>
  <div>
    <div class="container">
      <div class="form-group">
        <div class="input-group input-group-lg">
          <div class="input-group-prepend">
            <span class="input-group-text" id="inputGroup-sizing-lg">🔍</span>
          </div>
          <input
            type="text"
            class="form-control"
            aria-label="Large"
            aria-describedby="inputGroup-sizing-sm"
            v-model="search"
            placeholder="Gucci Gang, Gucci Gang, Gucci Gang."
          />
        </div>
        <div class="form-group">
          <button class="btn btn-primary m-2" @click="freshness = true">Sort by Freshness ❄️</button>
          <button class="btn btn-primary m-2" @click="freshness = false">Sort by Hotness 🔥</button>
        </div>
      </div>
    </div>
    <div class="container-fluid">
      <div class="card-columns">
        <div class="card p-4" v-for="r in ordered" :key="r.id">
          <div class="row">
            <blockquote class="blockquote mb-0 col-9">
              <p class="mb-0 text-wrap">{{swagify(r.transcript)}}</p>
               <footer class="blockquote-footer mb-2">
                <small class="text-muted">
                  {{r.name}}
                  <cite title="Source Title">{{rel(r.timestamp)}}</cite>
                </small>
               </footer>
              <p class="mb-0 text-wrap">{{swagify(r.answer)}}</p>
              <footer class="blockquote-footer">
                <small class="text-muted">
                  The Machine
                </small>
              </footer>
            </blockquote>
            <div class="col-3 d-flex flex-column">
              <button class="btn btn-primary" @click="vote(r.id,1)" :disabled="lock">👍</button>
              <h3 class="my-1">{{r.score}}</h3>
              <button class="btn btn-secondary" @click="vote(r.id,-1)" :disabled="lock">👎</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Fuse from "fuse.js";
import moment from "moment";
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: String,
      lock: false,
      search: "",
      freshness: true
    };
  },
  computed: {
    
    rhymes() {
      return this.$store.state.rhymes;
    },
    ordered() {
      var options = {
        keys: ["transcript", "name"],
        threshold: 0.3
      };
      var fuse = new Fuse(this.rhymes, options);
      if (this.search) {
        return fuse.search(this.search);
      } else if (this.freshness) {
        return this.rhymes.sort((a, b) => {
          return a.timestamp < b.timestamp;
        });
      } else {
        return this.rhymes.sort((a, b) => {
          return a.score < b.score;
        });
      }
    }
  },
  methods: {
    rel(timestamp) {
      return moment(timestamp).fromNow();
    },
    swagify(el){
      return el.replace('\n',` // `).replace('\n',` // `).replace('\n',` // `).replace('\n',` // `).replace('\n',` // `);
    },
    vote(id, val) {
      this.lock = true;
      this.$socket.emit("vote", {
        id: id,
        value: val
      });
      setTimeout(() => {
        this.lock = false;
      }, 2000);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
