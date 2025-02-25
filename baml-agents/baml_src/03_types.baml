class GetTasks {
  tool "getTasks"
  filter string @description("This can be either 'all' or 'pending'")
}

class AddTask {
  tool "addTask"
  title string
}

class MarkTaskAsDone {
  tool "markTaskAsDone"
}
