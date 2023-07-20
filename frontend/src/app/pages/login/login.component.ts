import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  login_form = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
  });
  constructor(private router: Router, private authService: AuthService) {}
  onSubmit() {
    this.authService
      .login(this.login_form.getRawValue())
      .subscribe((responseData: any) => {
        console.log(responseData);
        this.authService.accessToken = responseData.token;
        this.router.navigate(['/']);
      });
  }
}
