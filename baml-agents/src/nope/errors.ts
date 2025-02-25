export class Nope extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'Nope';
  }
}