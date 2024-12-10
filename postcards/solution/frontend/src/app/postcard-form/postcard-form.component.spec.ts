import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { PostcardService } from '../services/postcard.service';

import { PostcardFormComponent } from './postcard-form.component';

describe('PostcardFormComponent', () => {
  let component: PostcardFormComponent;
  let fixture: ComponentFixture<PostcardFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostcardFormComponent, HttpClientTestingModule],
      providers: [PostcardService]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostcardFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
