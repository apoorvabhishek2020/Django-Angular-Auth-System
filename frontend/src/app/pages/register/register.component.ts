import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent {
  register_form = new FormGroup({
    first_name: new FormControl(''),
    last_name: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
    password_confirm: new FormControl(''),
  });
  constructor(private router: Router, private authService: AuthService) {}
  onSubmit() {
    this.authService
      .register(this.register_form.getRawValue())
      .subscribe((responseData) => {
        console.log(responseData);
        this.router.navigate(['/login']);
      });
  }
}
