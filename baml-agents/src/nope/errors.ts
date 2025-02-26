export class NopeError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'Nope';
  }
}

export class NopeRetry extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NopeRetry';
  }
}
