import glob
import mimetypes
import sys

import os
from archive_api.models import NGTUser
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from archive_api.models import DataSet, get_upload_path, \
    DatasetArchiveField


class Command(BaseCommand):
    help = 'Upload a large data set archive file'

    def add_arguments(self, parser):
        parser.add_argument('ngt_id', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('archive_filename', type=str)

    def handle(self, *args, **options):

        archive_file = options['archive_filename']
        ngt_id = options['ngt_id']
        username = options['username']

        # Attempt to get the user
        try:
            # Get User
            user = NGTUser.objects.get(username=username)
            if not user.is_admin:
                raise CommandError('User "{}" is not an NGT administrator'.format(username))
        except User.DoesNotExist:
            raise CommandError('User "{}" does not exist'.format(username))

        # Determine if the file exists
        if os.path.exists(archive_file):
            try:
                # Find the dataset with the NGT id
                dataset = DataSet.objects.filter(ngt_id=ngt_id).order_by('-id')[0]

                # is this a valid content type?
                content_type, _ = mimetypes.guess_type(archive_file)
                if content_type in DatasetArchiveField.CONTENT_TYPES:
                    filename = get_upload_path(dataset, archive_file)
                    with open(archive_file, 'rb') as f:
                        dataset.archive.save(filename,
                                             File(f))
                    dataset.modified_by=user
                    dataset.save()
                    self.stdout.write('Archive file, {}, uploaded to data set {} v{}'.format(archive_file,
                                                                                             dataset.data_set_id(),

                                                                                          dataset.version), ending='\n')
                elif content_type is None:
                    raise CommandError('Unknown file type')
                else:
                    raise CommandError('{} is an invalid file type'.format(content_type))

            except DataSet.DoesNotExist:
                raise CommandError('NGT ID "{}" does not exist'.format(ngt_id))
            except Exception as e:
                raise CommandError('{}'.format(str(e)))
        else:
            raise CommandError('File {} does not exist'.format(archive_file))
