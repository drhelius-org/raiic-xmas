import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Postcard } from '../models/postcard.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PostcardService {
  constructor(private http: HttpClient) {}

  generatePostcard(data: { name: string; email: string; description: string }): Observable<Postcard> {
    return this.http.post<Postcard>('http://localhost:8000/generate_postcard', data);
  }

  sendPostcard(email: string, postcard: Postcard): Observable<void> {
    return this.http.post<void>('http://localhost:8000/send_postcard', { recipient_email: email, postcard });
  }
}