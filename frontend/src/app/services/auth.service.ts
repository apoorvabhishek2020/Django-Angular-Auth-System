import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  accessToken = '';
  constructor(private http: HttpClient, private router: Router) {}
  register(body: any) {
    return this.http.post(`${environment.api}/register`, body);
  }
  login(body: any) {
    return this.http.post(`${environment.api}/login`, body, {
      withCredentials: true,
    });
  }
  user() {
    return this.http.get(`${environment.api}/user`);
  }
}
