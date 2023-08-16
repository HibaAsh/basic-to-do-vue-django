<template>
  <div class="tasks_container">
    <div class="tasks_content">
        <h1>To-Do List</h1>
        <ul class="tasks_list">
            <li v-for="task in tasks" :key="task.id">
                <div class="task">
                    <h2>Title: {{ task.title }}</h2>
                    <p>Description: {{ task.description }}</p>
                    <p v-if="task.completed">Status: Done</p>
                    <p v-else>Status: In queue</p>
                    <div style="margin-bottom: 5%;"> 
                        <p style="display: inline;">Finished in: </p>
                        <p style="font-size: 12px; display: inline;">{{ task.full_time }}</p>
                    </div>
                    <button @click="modifyTask(task)">Edit</button>
                    <button @click="deleteTask(task)">Delete</button>
                </div>
            </li>
        </ul>
    </div>

    <div class="style_task" v-if="!update_task">
        <form v-on:submit.prevent="createTask">
            <h2>Create task</h2>
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" v-model="title">
            </div>
            <div class="form-group">
                <label for="description">Description</label>
                <textarea v-model="description"></textarea>
            </div>
            <div class="form-group">
                <button type="submit">Add Task</button>
            </div>
        </form>
    </div>

    <div class="style_task" v-if="update_task">
        <form v-on:submit.prevent="editTask(update_task)">
            <h2>Edit task</h2>
            <div class="form-group">
                <label>Title</label>
                <input type="text" v-model="update_task.title">
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea v-model="update_task.description"></textarea>
            </div>
            <div class="form-group">
                <label for="description">Completed</label>
                <input type="checkbox" v-model="update_task.completed">
            </div>
            <div class="form-group">
                <button type="submit">Edit Task</button>
            </div>
        </form>
    </div>
  </div>
</template>

<script>
export default {
    data(){
        return {
            tasks: [''],
            update_task: null,
            title: '',
            description: '',
            completed: false,
            created_at: '',
            finished_at: '',
            full_time: ''
        }
    },
    created() {
        this.getData()
    },
    methods: {
        async getData() {
            try {
                await this.$http
                .get('http://localhost:8000/task/')
                .then((response) => {
                    this.tasks = response.data;
                });
            } catch (error) {
                console.log(error);
            }
        },
        async modifyTask(task){
            this.update_task = task
        },
        async createTask() {
            console.log("inside create task function")
            try {
                await this.$http
                .post('http://localhost:8000/task/', {
                    title: this.title,
                    description: this.description,
                    completed: false, 
                    created_at: Date(Date.now())
                })
                .then((response) => {
                    // console.log("response.data: ", response.data)
                    this.tasks.push(response.data)
                    this.title = ''
                    this.description = ''
                    this.completed = false
                    this.created_at = ''
                });
            } catch (error) {
                console.log(error);
            }
        },
        async editTask(payload){
            let task = payload
            try {
                console.log("inside update task function")
                if ((task.completed) && (!task.full_time)){
                    console.log("created at: ", task.created_at)
                    task.finished_at = Date(Date.now())
                    console.log("finished at: ", task.finished_at)

                    let start_date = new Date(task.created_at).toLocaleDateString().split("/")
                    let start_month = parseInt(start_date[0])
                    let start_day = parseInt(start_date[1])
                    let start_year = parseInt(start_date[2])

                    let end_date = new Date(task.finished_at).toLocaleDateString().split("/")
                    let end_month = parseInt(end_date[0])
                    let end_day = parseInt(end_date[1])
                    let end_year = parseInt(end_date[2])

                    let start_time = new Date(task.created_at).toLocaleTimeString('en-GB').split(":")
                    let start_hour = parseInt(start_time[0])
                    let start_minute = parseInt(start_time[1])
                    let start_second = parseInt(start_time[2].split(" ")[0])

                    let end_time = new Date(task.finished_at).toLocaleTimeString('en-GB').split(":")
                    let end_second = parseInt(end_time[2].split(" ")[0])
                    let end_minute = parseInt(end_time[1])
                    let end_hour = parseInt(end_time[0])

                    if (end_second < start_second){
                        end_second += 60
                        end_minute -= 1
                    }
                    if (end_minute < start_minute){
                        end_minute += 60
                        end_hour -= 1
                    }
                    console.log("end hour: ", end_hour, "start hour: ", start_hour)
                    if (end_hour < start_hour){
                        // console.log("end hour is less...")
                        end_hour += 24
                        end_day -= 1
                    }
                    if (end_hour == 0){ // for midnight
                        end_hour = 24
                    }
                    if (end_day < start_day){
                        end_day += 30
                        end_month -= 1
                    }
                    if (end_month < start_month){
                        end_month += 30
                        end_year -= 1
                    }

                    let year = (end_year - start_year)
                    let month = (end_month - start_month)
                    let day = (end_day - start_day)
                    console.log(start_date, end_date)
                    console.log("date: ", year, month, day)

                    console.log("final time: ", end_second, end_minute, end_hour)

                    let hour = (end_hour - start_hour)
                    let minute = (end_minute - start_minute)
                    let second = (end_second - start_second)
                    console.log(start_time, end_time)
                    console.log("time: ", hour, minute, second)

                    task.full_time = year + " year, " + month + " month, " + day + " day, " + hour + "h " + minute + "m " + second + "s "
                }
                if(task.completed) {this.status = "Completed"}
                else if(task.completed) {this.status = "Not completed"}
                await this.$http
                .put('http://localhost:8000/task/' + task.id + '/', {
                    title: task.title,
                    description: task.description,
                    completed: task.completed,
                    created_at: task.created_at,
                    finished_at: task.finished_at,
                    full_time: task.full_time
                })
                .then((response) => {
                    console.log(response)

                    this.title = ''
                    this.description = ''
                    this.completed = false
                    this.created_at = '',
                    this.finished_at = '',
                    this.full_time = ''
                    this.update_task = null
                    this.getData()
                });
            } catch (error) {
                console.log(error);
            }
        },
        async deleteTask(task){
            console.log("inside delete task function")
            try{
                await this.$http.delete('http://localhost:8000/task/' + task.id + '/')
                this.getData()
            }
            catch(err){
                console.log(err)
            }
        },

    },
    
}
</script>

<style>
    .tasks_container{
        width: 100%;
    }
    .tasks_content h1{
        color: rgb(243, 79, 142);
        /* border-bottom: 1px solid red; */
        /* width: 30%; */
        margin: 20px auto;
        font-size: 40px;
    }
    .tasks_list{
        width: 95%;
        padding: 20px;
        margin: auto;
        list-style: none;
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        grid-auto-rows: 1fr;
        grid-column-gap: 20px; 
        /* grid-row-gap: 30px; */
        border: 1px solid rgb(243, 79, 142); 
        /* background: rgb(174, 240, 252, 0.5); */

        /* width: 50%;  */
    }
    .tasks_list h2, .style_task h2{
        color: rgb(243, 79, 142, 0.7);
        /* margin: 30px; */
        font-size: 20px;
    }
    .tasks_list li{
        /* border: 1px solid red; */
        text-align: center;
    }
    .task{
        text-align: center;
        /* border-bottom: 1px solid rgb(243, 79, 142); */
        padding: 30px;
        background: rgba(255, 255, 255, 0.5);
        /* color: rgba(243, 79, 142, 0.7); */
        margin: 10px;
        height: 70%;
    }
    button{
        border: none;
        margin: auto 10px;
        background: none;
        background: #F4D7E3;
        padding: 10px;
        /* color: white; */
    }
    button:active{
        background: rgb(243, 79, 142);
    }
    .style_task{
        width: 95%;
        border: 1px solid rgb(243, 79, 142); 
        /* background: rgb(174, 240, 252, 0.5); */
        margin: auto;
        padding: 20px;
    }
    /* .style_task h3{
        font-size: 25px;
        color: rgb(66, 85, 250);
    } */
    form{
        background: rgba(255, 255, 255, 0.6);
        margin: auto;
        padding: 10px;
    }
    .form-group{
        text-align: center;
    }
    .form-group label{
        display: block;
        padding: 10px 0;
        text-align: center;
    }
    .form-group input, textarea{
        width: 50%;
        padding: 10px 0;
        margin: 10px; 
        padding: 5px;
    }
    .form-group button{
        width: 30%;
        padding: 10px 0;
        margin: 10px; 
    }
</style>