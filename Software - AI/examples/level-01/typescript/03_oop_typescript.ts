abstract class Account {
  constructor(public readonly name: string, protected balance: number) {}
  deposit(amount: number) { this.balance += amount; }
  abstract summary(): string;
}

class SavingsAccount extends Account {
  summary(): string { return `${this.name}: BDT ${this.balance}`; }
}

const account = new SavingsAccount("Saiful", 5000);
account.deposit(750);
console.log(account.summary());
