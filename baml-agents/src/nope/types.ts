export class Context<DepsT = undefined> {
  public readonly retries: number;
  public readonly deps: DepsT

  constructor(deps: DepsT, retries: number = 3) {
    this.deps = deps;
    this.retries = retries;
  }
}

export class AgentRequest<T> {
  args: T;

  constructor(args: T) {
    this.args = args;
  }
}

export class AgentResponse<T> {
  data: T;

  constructor(data: T) {
    this.data = data;
  }
}
