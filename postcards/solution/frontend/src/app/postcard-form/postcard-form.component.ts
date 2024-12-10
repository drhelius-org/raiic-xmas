import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { PostcardService } from '../services/postcard.service';
import { Postcard } from '../models/postcard.model';

@Component({
  selector: 'app-postcard-form',
  standalone: true,
  imports: [FormsModule, NgIf],
  templateUrl: './postcard-form.component.html',
  styleUrl: './postcard-form.component.css'
})
export class PostcardFormComponent {
  name: string = '';
  email: string = '';
  description: string = '';
  postcard: Postcard | null = null;

  constructor(private postcardService: PostcardService) {}

  onSubmit() {
    const requestData = {
      name: this.name,
      email: this.email,
      description: this.description
    };
    this.postcardService.generatePostcard(requestData)
      .subscribe(postcard => {
        this.postcard = postcard;
      });
  }

  sendPostcard() {
    if (this.postcard) {
      this.postcardService.sendPostcard(this.email, this.postcard)
        .subscribe();
    }
  }
}
